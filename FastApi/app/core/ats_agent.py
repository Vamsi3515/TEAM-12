"""ATS analyzer agent with RAG + Gemini."""

import json
from typing import Dict, List, Tuple, Optional

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
{{
  "ats_score": 0-100,
  "rejection_reasons": ["string"],
  "strengths": ["string"],
  "issues": ["string"],
  "actionable_suggestions": ["string"],
  "summary": "string",
}}

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

    # Add evidence from RAG
    evidence_snippets = [{"id": i, "snippet": d[:300]} for i, d in zip(ids, docs)]

    return ATSAnalyzeOutput(
        ats_score=int(data.get("ats_score", 50)),
        rejection_reasons=list(data.get("rejection_reasons", [])),
        strengths=list(data.get("strengths", [])),
        issues=list(data.get("issues", [])),
        actionable_suggestions=list(data.get("actionable_suggestions", [])),
        summary=str(data.get("summary", "")),
    )
