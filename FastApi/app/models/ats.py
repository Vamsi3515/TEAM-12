from typing import List, Optional
from pydantic import BaseModel


class ATSAnalyzeInput(BaseModel):
    """Input schema for ATS analysis."""
    resume_text: str
    job_description: Optional[str] = None
    email: Optional[str] = None


class ATSAnalyzeOutput(BaseModel):
    """Output schema for ATS analysis results."""
    ats_score: int
    rejection_reasons: List[str]
    strengths: List[str]
    issues: List[str]
    actionable_suggestions: List[str]
    summary: str
    sent_to_email: bool


__all__ = [
    "ATSAnalyzeInput",
    "ATSAnalyzeOutput",
]
