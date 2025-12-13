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
    sent_to_email: bool = False


# Security Audit (legacy)
class SecurityAuditRequest(BaseModel):
    code: str

class SecurityAuditResponse(BaseModel):
    findings: List[str]

# Security Audit (UI-facing)
class SecurityAuditInput(BaseModel):
    code: Optional[str] = ""
    repoUrl: Optional[str] = ""
    inputType: Optional[str] = "code"  # code | repo

class SecurityAuditSummary(BaseModel):
    critical: int
    high: int
    medium: int
    low: int

class SecurityVulnerability(BaseModel):
    title: str
    severity: str
    description: str
    fixes: List[str] = []
    cwe: Optional[str] = None

class SecurityAuditUIResponse(BaseModel):
    summary: SecurityAuditSummary
    vulnerabilities: List[SecurityVulnerability]
    recommendations: List[str]

class SecurityAuditOutput(BaseModel):
    """Output schema for security analysis matching agent return structure."""
    vulnerabilities: List[Dict]
    security_score: float  # 0-100, higher is better
    risk_score: float  # Risk points accumulated
    risk_level: str  # low, medium, high, critical
    summary: str
    evidence_ids: List[str]
    evidence_snippets: List[Dict]
