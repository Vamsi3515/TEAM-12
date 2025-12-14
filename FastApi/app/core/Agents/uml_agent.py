import json
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError

from app.core.Utils.llm_client import _call_gemini, _call_groq
from app.core.RAGANDEMBEDDINGS.vectorstore import get_or_create_collection
from app.core.RAGANDEMBEDDINGS.embeddings import embed
from app.core.RAGANDEMBEDDINGS.uml_rag_data import uml_knowledge

# --------- Limits & Defaults ---------
MAX_DESC_LEN = 2000
MAX_RAG_LEN = 2000
MAX_RAW_LEN = 4000
MAX_MERMAID_LEN = 1200
MAX_TEXT_LEN = 200
MAX_DIAGRAMS = 4


# --------- Pydantic Schemas ---------
class DiagramModel(BaseModel):
    type: str = Field(..., pattern="^(class|sequence|flowchart|erd|dependency)$")
    title: str = Field("", max_length=MAX_TEXT_LEN)
    mermaid: str = Field("", max_length=MAX_MERMAID_LEN)
    description: str = Field("", max_length=MAX_TEXT_LEN)


class ApiRouteModel(BaseModel):
    method: str = Field("GET", max_length=10)
    path: str = Field("/", max_length=200)
    description: str = Field("", max_length=MAX_TEXT_LEN)


class SummaryModel(BaseModel):
    classesCount: int = Field(0, ge=0)
    endpointsCount: int = Field(0, ge=0)
    dependenciesCount: int = Field(0, ge=0)
    architectureType: str = Field("unknown", max_length=50)
    complexity: str = Field("unknown", max_length=20)
    languages: List[str] = Field(default_factory=list)


class UMLResponseModel(BaseModel):
    diagrams: List[DiagramModel] = Field(default_factory=list, max_items=MAX_DIAGRAMS)
    apiRoutes: List[ApiRouteModel] = Field(default_factory=list)
    folderStructure: str = Field("", max_length=1000)
    summary: SummaryModel = Field(default_factory=SummaryModel)

# seed UML knowledge into vector DB
def seed_uml_collection():
    col = get_or_create_collection("uml_knowledge")
    if col.count() == 0:
        texts = [x["text"] for x in uml_knowledge]
        ids = [x["id"] for x in uml_knowledge]
        emb = embed(texts)
        col.add(documents=texts, ids=ids, embeddings=emb)
    return col

def retrieve_uml_context(query: str, k=3):
    try:
        col = seed_uml_collection()
        q_emb = embed([query])[0]
        res = col.query(query_embeddings=[q_emb], n_results=k)

        docs = res.get("documents", [[]])[0] if res else []
        ids = res.get("ids", [[]])[0] if res else []
        if not docs:
            return ""
        rag_context = "\n\n".join([f"ID:{ids[i] if i < len(ids) else f'kb-{i}'}\n{docs[i]}" for i in range(len(docs))])
        return rag_context[:MAX_RAG_LEN]
    except Exception:
        return ""


async def generate_uml(description: str, uml_type: str = "auto"):
    # Retrieve grounding context (best effort)
    safe_description = (description or "").strip()[:MAX_DESC_LEN]
    rag_context = retrieve_uml_context(safe_description)

    # Build LLM prompt asking for multiple diagrams and architecture summary
    prompt = f"""You are an expert software architect and UML designer.

User Description:
{safe_description}

Requested UML type: {uml_type}

Use the provided UML best-practices and examples for grounding:
{rag_context}

Produce a comprehensive architecture analysis and multiple Mermaid diagrams covering the most useful views for this codebase. The output MUST be a single JSON object matching this EXACT schema (no markdown, no code fences, no extra text):

{{
    "diagrams": [
        {{
            "type": "class|sequence|flowchart|erd|dependency",
            "title": "string",
            "mermaid": "string",    // mermaid diagram text with newlines escaped as \n
            "description": "string"
        }}
    ],
    "apiRoutes": [ {{ "method": "GET|POST|PUT|DELETE", "path": "/api/..", "description": "string" }} ],
    "folderStructure": "string (tree view)",
    "summary": {{
            "classesCount": int,
            "endpointsCount": int,
            "dependenciesCount": int,
            "architectureType": "monolith|microservices|serverless|unknown",
            "complexity": "low|medium|high",
            "languages": ["python","js"]
    }}
}}

Rules:
1) Return ONLY the JSON object exactly matching the schema (no markdown, no code fences).
2) Provide at least two diagrams (if possible): one structural (class/dependency) and one behavioral (sequence/flowchart).
3) Limit diagrams to at most 4 items; each mermaid string <= 1200 characters; titles/descriptions <= 200 characters.
4) Escape newlines in mermaid as \n; do not include backticks or fencing.
5) Populate summary fields with best-effort counts and inferred architectureType and complexity.
6) Do NOT invent external URLs or secrets; only use info provided by the user or grounding context.

Begin.
"""

    raw = await _call_groq(prompt, model="llama-3.3-70b-versatile", max_tokens=1600, temperature=0.15)

    cleaned = raw.strip()[:MAX_RAW_LEN]
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()

    # Try to parse JSON; if parsing fails, attempt a repair call; otherwise provide minimal fallback
    def _fallback_payload():
        return {
            "diagrams": [
                {
                    "type": "class",
                    "title": "Class Diagram",
                    "mermaid": "classDiagram\\n  class A {\\n    +method()\\n  }\\n",
                    "description": "Fallback class diagram"
                },
                {
                    "type": "flowchart",
                    "title": "Flow Diagram",
                    "mermaid": "flowchart TD\\n  A[Start] --> B[Process]\\n  B --> C[End]",
                    "description": "Fallback flow diagram"
                }
            ],
            "apiRoutes": [],
            "folderStructure": "",
            "summary": {
                "classesCount": 0,
                "endpointsCount": 0,
                "dependenciesCount": 0,
                "architectureType": "unknown",
                "complexity": "unknown",
                "languages": ["unknown"]
            }
        }

    def _coerce_and_bound(data: dict) -> dict:
        try:
            validated = UMLResponseModel(**data)
        except ValidationError:
            # Attempt best-effort clipping then retry
            data = data or {}
            data.setdefault("diagrams", [])
            data["diagrams"] = data["diagrams"][:MAX_DIAGRAMS]
            for d in data["diagrams"]:
                if isinstance(d, dict):
                    d["title"] = str(d.get("title", ""))[:MAX_TEXT_LEN]
                    d["description"] = str(d.get("description", ""))[:MAX_TEXT_LEN]
                    d["mermaid"] = str(d.get("mermaid", ""))[:MAX_MERMAID_LEN]
            data.setdefault("apiRoutes", [])
            data.setdefault("folderStructure", "")
            data.setdefault("summary", {})
            data["folderStructure"] = str(data["folderStructure"])[:1000]
            try:
                validated = UMLResponseModel(**data)
            except ValidationError:
                validated = UMLResponseModel(**_fallback_payload())
        # Convert back to primitive dict
        return json.loads(validated.model_dump_json())

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        repair_prompt = (
            "The previous response was not valid JSON. Reformat it strictly as JSON matching the schema. "
            "Return only JSON, no markdown."
            f" Previous response:\n{cleaned}"
        )
        repaired = await _call_groq(repair_prompt, model="llama-3.3-70b-versatile", max_tokens=800, temperature=0.0)
        repaired_clean = repaired.strip()[:MAX_RAW_LEN]
        if repaired_clean.startswith("```"):
            lines = repaired_clean.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            repaired_clean = "\n".join(lines).strip()
        try:
            parsed = json.loads(repaired_clean)
        except Exception:
            parsed = _fallback_payload()

    bounded = _coerce_and_bound(parsed)
    return bounded