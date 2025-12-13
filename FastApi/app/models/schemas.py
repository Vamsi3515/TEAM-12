from pydantic import BaseModel
from typing import List, Dict, Optional

class GitHubAnalyzeInput(BaseModel):
    repoUrl: str  # Accept camelCase from frontend

class GitHubMetric(BaseModel):
    name: str
    score: float
    explanation: str

class GitHubAnalyzeOutput(BaseModel):
    tech_stack: List[str]
    metrics: List[GitHubMetric]
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    repo_summary: str
    evidence_ids: List[str]  # RAG evidence
    evidence_snippets: List[Dict[str, str]]  # RAG evidence snippets

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
