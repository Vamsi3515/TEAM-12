"""Schema definitions for Experience Authenticity & Skill Consistency Agent."""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ResumeData(BaseModel):
    """Structured resume information."""
    full_name: Optional[str] = None
    skills: List[str] = []
    experience: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    education: List[Dict[str, Any]] = []
    certifications: List[str] = []
    raw_text: Optional[str] = None


class GitHubEvidence(BaseModel):
    """Evidence from GitHub profile analysis."""
    username: Optional[str] = None
    languages: List[str] = []
    repo_count: int = 0
    commit_frequency: str = "unknown"  # high, medium, low
    top_projects: List[Dict[str, Any]] = []
    readme_quality: str = "unknown"  # excellent, good, fair, poor
    contribution_pattern: str = "unknown"  # consistent, sporadic, recent
    raw_profile_data: Optional[Dict[str, Any]] = None


class LeetCodeEvidence(BaseModel):
    """Evidence from LeetCode profile if available."""
    problems_solved: int = 0
    difficulty_distribution: Dict[str, int] = {}  # {"Easy": 50, "Medium": 30, "Hard": 10}
    recent_activity: bool = False
    ranking: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None


class SkillAlignment(BaseModel):
    """Individual skill alignment analysis."""
    skill: str
    confidence: str  # "High", "Medium", "Low"
    evidence_source: List[str] = []  # ["Resume", "GitHub", "LeetCode"]
    supporting_evidence: List[str] = []
    gap_analysis: Optional[str] = None


class AuthenticityAnalysisInput(BaseModel):
    """Input for authenticity analysis."""
    resume: ResumeData
    github: Optional[GitHubEvidence] = None
    leetcode: Optional[LeetCodeEvidence] = None
    additional_context: Optional[str] = None


class AuthenticityAnalysisOutput(BaseModel):
    """Output from authenticity analysis (STRICT JSON format)."""
    confidence_level: str  # "High", "Medium", "Low"
    authenticity_score: float  # 0-100
    strong_evidence: List[str]  # Supported skills and positive signals
    risk_indicators: List[str]  # Weak or missing evidence areas
    overall_assessment: str  # Short, neutral explanation
    improvement_suggestions: List[str]  # Actionable steps
    skill_alignments: List[SkillAlignment] = []  # Detailed skill-by-skill analysis
    confidence_breakdown: Dict[str, Any] = {}  # Internal scoring details (optional)

# ==================== New Schemas: Evidence & Claims ====================

class EvidenceItem(BaseModel):
    """Generic supportive evidence object from frontend (unbounded)."""
    type: str  # github_repo | github_profile | leetcode_profile | portfolio | blog | kaggle | certificate | link | other
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    metadata: Dict[str, Any] = {}


class Claim(BaseModel):
    """Normalized verifiable claim."""
    kind: str  # skill | project | certification | participation | ranking | achievement | username | link
    text: str
    normalized: Optional[str] = None
    source: str  # resume | user | evidence
    extracted_from: Optional[str] = None  # e.g., resume section, evidence url


class ClaimEvidenceMapping(BaseModel):
    """Mapping of a claim to one or more evidences with evaluation."""
    evidence: EvidenceItem
    relevance: float  # 0-1
    strength: float  # 0-1
    directness: float  # 0-1
    notes: Optional[str] = None


class ClaimVerification(BaseModel):
    """Verification result per claim with confidence scoring."""
    claim: Claim
    status: str  # Verified | Partially Verified | Unverified | Contradicted | Inconclusive
    confidence: float  # 0-100
    mapped_evidence: List[ClaimEvidenceMapping] = []
    rag_checks: List[str] = []  # notes from RAG lookups
    flags: List[str] = []  # suspicious indicators without accusatory wording


class AuthenticityExtendedInput(BaseModel):
    """Extended input including dynamic evidence list."""
    resume: ResumeData
    github: Optional[GitHubEvidence] = None
    leetcode: Optional[LeetCodeEvidence] = None
    evidences: List[EvidenceItem] = []
    additional_context: Optional[str] = None


class AuthenticityExtendedOutput(AuthenticityAnalysisOutput):
    """Extended output including per-claim verification results."""
    extracted_claims: List[Claim] = []
    claim_verifications: List[ClaimVerification] = []
