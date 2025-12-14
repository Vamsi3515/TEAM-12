from fastapi import APIRouter
from app.models.ats import ATSAnalyzeInput, ATSAnalyzeOutput
from app.core.Agents.ats_agent import analyze_ats as analyze_ats_core

router = APIRouter(tags=["ATS Analyzer"])


@router.post("/analyze-ats", response_model=ATSAnalyzeOutput)
async def analyze_ats(input_data: ATSAnalyzeInput) -> ATSAnalyzeOutput:
    """Analyze resume against optional job description and produce ATS report using RAG + Gemini."""
    return await analyze_ats_core(
        resume_text=input_data.resume_text,
        job_description=input_data.job_description,
        email=input_data.email,
    )
