import json
from app.core.llm_client import _call_gemini, _call_groq

from app.core.vectorstore import get_or_create_collection
from app.core.embeddings import embed
from app.core.uml_rag_data import uml_knowledge

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
    col = seed_uml_collection()
    q_emb = embed([query])[0]
    res = col.query(query_embeddings=[q_emb], n_results=k)

    docs = res["documents"][0]
    ids = res["ids"][0]

    rag_context = "\n\n".join([f"ID:{ids[i]}\n{docs[i]}" for i in range(len(docs))])
    return rag_context


async def generate_uml(description: str, uml_type: str = "auto"):

    # Retrieve grounding context
    rag_context = retrieve_uml_context(description)

        # Build LLM prompt asking for multiple diagrams and architecture summary
    prompt = f"""You are an expert software architect and UML designer.

User Description:
{description}

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
1) Return ONLY the JSON object exactly matching the schema.
2) Provide at least two diagrams (if possible): one structural (class/dependency) and one behavioral (sequence/flowchart).
3) For mermaid diagrams, escape newlines as \n.
4) Populate summary fields with best-effort counts and inferred architectureType and complexity.
5) If repository URL was provided, include repository-specific notes in explanation fields.

Begin.
"""

    raw = await _call_groq(prompt, model="llama-3.3-70b-versatile", max_tokens=1600, temperature=0.15)

    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()

    # Try to parse JSON; if parsing fails, attempt a repair call; otherwise provide minimal fallback
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        repair_prompt = f"The previous response was not valid JSON. Reformat it strictly as JSON matching the schema. Previous response:\n{cleaned}"
        repaired = await _call_groq(repair_prompt, model="llama-3.3-70b-versatile", max_tokens=800, temperature=0.0)
        repaired_clean = repaired.strip()
        if repaired_clean.startswith("```"):
            lines = repaired_clean.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            repaired_clean = "\n".join(lines).strip()
        try:
            parsed = json.loads(repaired_clean)
        except Exception:
            # fallback: return minimal set with two simple diagrams
            parsed = {
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

    # Normalize minimal fields to avoid runtime errors
    parsed.setdefault("diagrams", parsed.get("diagrams", []))
    parsed.setdefault("apiRoutes", parsed.get("apiRoutes", []))
    parsed.setdefault("folderStructure", parsed.get("folderStructure", ""))
    parsed.setdefault("summary", parsed.get("summary", {
        "classesCount": 0,
        "endpointsCount": 0,
        "dependenciesCount": 0,
        "architectureType": "unknown",
        "complexity": "unknown",
        "languages": ["unknown"]
    }))

    return parsed