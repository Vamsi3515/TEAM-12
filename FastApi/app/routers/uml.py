from fastapi import APIRouter
from app.models.schemas import UMLRequest, UMLResponse, CodeDiagramInput, CodeDiagramUIOutput
from app.core.Agents.uml_agent import generate_uml

router = APIRouter(prefix="", tags=["UML Generator"])

@router.post("/uml", response_model=UMLResponse)
async def uml_generator(req: UMLRequest):
    """Generate UML diagram from description."""
    return await generate_uml(req.description, req.uml_type)


@router.post("/generate-code-diagrams", response_model=CodeDiagramUIOutput)
async def generate_code_diagrams(req: CodeDiagramInput):
    """Generate UML diagram from code or repository."""
    # Build description from input
    if req.inputType == "repo" and req.repoUrl:
        description = f"Generate a UML architecture diagram for the repository at: {req.repoUrl}"
    else:
        # Use code snippet to infer diagram type
        code_preview = (req.code or "")[:500]
        description = f"Generate a UML class diagram from this code:\n\n{code_preview}"
    
    # Auto-detect best UML type from code
    uml_type = "auto"
    if "class " in (req.code or "").lower() or "def " in (req.code or "").lower():
        uml_type = "class"
    elif "def " in (req.code or "").lower() and "->" in (req.code or ""):
        uml_type = "sequence"
    elif "database" in (req.code or "").lower() or "table" in (req.code or "").lower():
        uml_type = "erd"
    
    # Generate UML and extended architecture output (multiple diagrams)
    result = await generate_uml(description, uml_type)

    # Return the parsed structure directly (Pydantic will validate)
    return CodeDiagramUIOutput(**result)
