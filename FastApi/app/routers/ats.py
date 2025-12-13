from fastapi import APIRouter
from app.models.ats import ATSAnalyzeInput, ATSAnalyzeOutput

router = APIRouter(tags=["ATS Analyzer"])


@router.post("/analyze-ats", response_model=ATSAnalyzeOutput)
async def analyze_ats(input_data: ATSAnalyzeInput) -> ATSAnalyzeOutput:
    """Analyze resume against optional job description and produce ATS report.

    Replace the placeholder logic with your actual analyzer.
    """
    # Placeholder implementation; integrate your analyzer here
    ats_score = 70
    rejection_reasons = [
        "Missing keywords from job description" if input_data.job_description else ""
    ]
    rejection_reasons = [r for r in rejection_reasons if r]

    strengths = ["Clear formatting", "Consistent section headings"]
    issues = ["Lacks quantified achievements"]
    actionable_suggestions = [
        "Add role-specific keywords",
        "Quantify impact with metrics",
        "Include links to portfolio or GitHub",
    ]
    summary = "Resume is generally solid; add targeted keywords and quantify achievements to improve ATS score."
    sent_to_email = bool(input_data.email)

    return ATSAnalyzeOutput(
        ats_score=ats_score,
        rejection_reasons=rejection_reasons,
        strengths=strengths,
        issues=issues,
        actionable_suggestions=actionable_suggestions,
        summary=summary,
        sent_to_email=sent_to_email,
    )
