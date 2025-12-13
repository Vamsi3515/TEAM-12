"""ATS analyzer agent with RAG + Gemini and email delivery."""

import json
import os
import smtplib
from email.message import EmailMessage
from typing import List, Tuple, Optional

from app.core.embeddings import embed
from app.core.vectorstore import get_or_create_collection
from app.core.ats_data import ats_data
from app.core.llm_client import _call_gemini
from app.models.ats import ATSAnalyzeOutput


COLLECTION_NAME = "ats_knowledge"


def seed_ats_collection(name: str = COLLECTION_NAME) -> int:
    """Seed ats_data into ChromaDB collection if empty.

    Returns number of documents currently in the collection after seeding.
    """
    col = get_or_create_collection(name)
    count = col.count()
    if count > 0:
        return count

    texts = [item["text"] for item in ats_data]
    ids = [item["id"] for item in ats_data]
    embeddings = embed(texts)
    col.add(documents=texts, ids=ids, embeddings=embeddings)
    return col.count()


def retrieve_ats_context(resume_text: str, job_description: Optional[str] = None, n_results: int = 4) -> Tuple[List[str], List[str]]:
    """Retrieve top relevant snippets for resume + optional job description.

    Returns (ids, documents).
    """
    col = get_or_create_collection(COLLECTION_NAME)
    if col.count() == 0:
        seed_ats_collection(COLLECTION_NAME)

    query = resume_text
    if job_description:
        query += "\nJob Description:\n" + job_description

    q_emb = embed([query])[0]
    res = col.query(query_embeddings=[q_emb], n_results=n_results)

    ids = res.get("ids", [[]])[0] if res else []
    docs = res.get("documents", [[]])[0] if res else []
    return ids, docs


def build_prompt(resume_text: str, job_description: Optional[str], context_docs: List[str]) -> str:
    """Compose the LLM prompt using resume, JD, and RAG context."""
    context_block = "\n\n".join([f"[Source {i+1}] {doc}" for i, doc in enumerate(context_docs, 1)]) or "(No context found)"
    jd_block = job_description or "(Not provided)"
    return f"""You are an ATS analysis assistant. Read the resume and optional job description, using the best-practice context to score and critique.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_block}

BEST-PRACTICE CONTEXT (RAG):
{context_block}

Return ONLY valid JSON with this exact schema:
{
    "ats_score": 0-100,
    "rejection_reasons": ["string"],
    "strengths": ["string"],
    "issues": ["string"],
    "actionable_suggestions": ["string"],
    "summary": "string",
    "sent_to_email": true
}

Rules:
- Keep ats_score integer 0-100.
- Use concise, specific bullet points for lists.
- Do not wrap in markdown or code fences.
- Do not add commentary outside the JSON.
"""


def _strip_code_fences(text: str) -> str:
    if "```" not in text:
        return text.strip()
    parts = text.split("```")
    # take content between first pair if present
    if len(parts) >= 3:
        return parts[1].strip()
    return text.replace("```json", "").replace("```", "").strip()


def _send_email(to_email: str, summary: str, rejection_reasons: List[str], suggestions: List[str], ats_score: int) -> bool:
    """Send rejection email with reasons and suggestions. Returns success flag."""
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_FROM", user or "noreply@example.com")

    if not host or not user or not password:
        print("[ATS Email] SMTP settings missing; skipping email send")
        return False

    body_lines = [
        f"ATS Score: {ats_score}",
        "",
        "Summary:",
        summary,
        "",
        "Rejection Reasons:",
        *((f"- {r}" for r in rejection_reasons) if rejection_reasons else ["- None provided"]),
        "",
        "Actionable Suggestions:",
        *((f"- {s}" for s in suggestions) if suggestions else ["- None provided"]),
    ]
    
    body = "\n".join(body_lines)

    msg = EmailMessage()
    msg["Subject"] = "Your ATS Analysis Results"
    msg["From"] = sender
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(host, port, timeout=15) as smtp:
            smtp.starttls()
            smtp.login(user, password)
            smtp.send_message(msg)
        return True
    except Exception as exc:
        print(f"[ATS Email] Send failed: {exc}")
        return False


async def analyze_ats(resume_text: str, job_description: Optional[str] = None, email: Optional[str] = None) -> ATSAnalyzeOutput:
    """Main ATS analysis pipeline using RAG + Gemini."""
    # Step 1: retrieve context
    ids, docs = retrieve_ats_context(resume_text, job_description, n_results=4)

    # Step 2: build prompt
    prompt = build_prompt(resume_text, job_description, docs)

    # Step 3: call Gemini
    raw = await _call_gemini(prompt, model="gemini-2.5-flash", max_tokens=800, temperature=0.4)

    # Step 4: clean fences
    cleaned = _strip_code_fences(raw or "")

    # Step 5: parse JSON with fallback
    try:
        data = json.loads(cleaned)
    except Exception:
        data = {
            "ats_score": 50,
            "rejection_reasons": ["Could not parse LLM response"],
            "strengths": [],
            "issues": [],
            "actionable_suggestions": ["Retry analysis"],
            "summary": "Partial analysis; parsing failed.",
        }

    # Ensure required fields with defaults
    data.setdefault("ats_score", 50)
    data.setdefault("rejection_reasons", [])
    data.setdefault("strengths", [])
    data.setdefault("issues", [])
    data.setdefault("actionable_suggestions", [])
    data.setdefault("summary", "")
    data.setdefault("sent_to_email", False)

    # Optionally send email
    sent_flag = False
    if email:
        sent_flag = _send_email(
            to_email=email,
            summary=str(data.get("summary", "")),
            rejection_reasons=list(data.get("rejection_reasons", [])),
            suggestions=list(data.get("actionable_suggestions", [])),
            ats_score=int(data.get("ats_score", 50)),
        )

    return ATSAnalyzeOutput(
        ats_score=int(data.get("ats_score", 50)),
        rejection_reasons=list(data.get("rejection_reasons", [])),
        strengths=list(data.get("strengths", [])),
        issues=list(data.get("issues", [])),
        actionable_suggestions=list(data.get("actionable_suggestions", [])),
        summary=str(data.get("summary", "")),
        sent_to_email=sent_flag,
    )
