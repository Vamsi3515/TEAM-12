from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class PortfolioInput(BaseModel):
    name: str
    title: str
    summary: str
    skills: str
    projects: Optional[str] = ""
    experience: Optional[str] = ""
    education: Optional[str] = ""
    contactEmail: Optional[str] = ""

class PortfolioOutput(BaseModel):
    html: str


# Generic LLM request/response for llm_generic router
class GenerationParameters(BaseModel):
    max_new_tokens: int = 512
    temperature: float = 0.7


class GenericIn(BaseModel):
    inputs: str
    parameters: GenerationParameters = GenerationParameters()


class GenericOut(BaseModel):
    generated_text: str


# Learning Flow
class LearningPlanRequest(BaseModel):
    goal: str
    background: Optional[str] = None
    timeframe_weeks: int = 4


class LearningNextStepsResponse(BaseModel):
    steps: List[str]


# GitHub Analyzer
class RepoAnalyzeRequest(BaseModel):
    repo_url: str


class RepoAnalyzeResponse(BaseModel):
    summary: str


# Learning Flow Generator
class LearningFlowRequest(BaseModel):
    topic: str
    experience_level: str  # beginner, intermediate, advanced
    weekly_hours: str      # 1-5, 5-10, 10-20, 20+


class LearningPhase(BaseModel):
    name: str
    duration: str
    description: str
    topics: List[str]


class YouTubeChannel(BaseModel):
    name: str
    url: str
    focus: str
    recommended_playlists: List[str]


class ProjectRecommendation(BaseModel):
    name: str
    description: str
    difficulty: str  # beginner, intermediate, advanced
    estimated_hours: int


class LearningResources(BaseModel):
    books: List[str]
    websites: List[str]
    communities: List[str]


class TimelineInfo(BaseModel):
    weeks: float
    total_hours: int
    avg_hours_per_week: float


class RAGEvidence(BaseModel):
    title: str
    snippet: str


class LearningFlowResponse(BaseModel):
    phases: List[LearningPhase]
    mermaid_flowchart: str
    youtube_channels: List[YouTubeChannel]
    projects: List[ProjectRecommendation]
    prerequisites: List[str]
    resources: LearningResources
    timeline: TimelineInfo
    rag_evidence: Optional[List[RAGEvidence]] = []
    languages: Optional[Dict[str, int]] = None


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


# Resume Extraction
class ResumeExtractRequest(BaseModel):
    text: Optional[str] = None


class ResumeExtractResponse(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]
    summary: Optional[str]

class ResumeTextResponse(BaseModel):
    text: str


# Skill Gap
class SkillGapRequest(BaseModel):
    job_description: str
    resume_text: str


class SkillGapResponse(BaseModel):
    strengths: List[str]
    gaps: List[str]
    recommendations: List[str]

class StudyPhaseUI(BaseModel):
    phase: str
    duration: str
    topics: List[str]
    resources: List[str] = []

class SkillGapUIInput(BaseModel):
    resume: Optional[str] = ""
    jobDescription: Optional[str] = ""
    jobDescriptionUrl: Optional[str] = ""
    inputType: Optional[str] = "text"  # text | url

class SkillGapUIOutput(BaseModel):
    overallGap: int
    skillMatch: int
    experienceMatch: int
    matchingSkills: List[str]
    missingHardSkills: List[str]
    missingSoftSkills: List[str]
    requiredExperience: str
    candidateExperience: str
    experienceGap: str
    industryMatch: str
    domainAlignment: str
    studyPath: List[StudyPhaseUI]
    recommendations: List[str]


# Code Diagrams
class CodeDiagramRequest(BaseModel):
    code: str


class CodeDiagramResponse(BaseModel):
    format: str
    content: str

# Code to UML (UI-facing)
class CodeDiagramInput(BaseModel):
    code: Optional[str] = ""
    repoUrl: Optional[str] = ""
    inputType: Optional[str] = "code"  # code | repo

class DiagramItem(BaseModel):
    type: str
    title: str
    mermaid: str
    description: Optional[str] = ""


class ArchitectureSummary(BaseModel):
    classesCount: int = 0
    endpointsCount: int = 0
    dependenciesCount: int = 0
    architectureType: str = "Unknown"
    complexity: str = "Unknown"
    languages: List[str] = ["Unknown"]


class CodeDiagramUIOutput(BaseModel):
    diagrams: List[DiagramItem]
    apiRoutes: Optional[List[Dict[str, str]]] = []
    folderStructure: Optional[str] = ""
    summary: ArchitectureSummary

class SkillGapInput(BaseModel):
    resume_text: str
    job_description: str

class SkillGapOutput(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    score: float
    recommended_learning_path: List[str]
    final_summary: str


class CareerPathInput(BaseModel):
    current_role: str
    target_role: str
    years_of_experience: Optional[float] = 0.0
    constraints: Optional[str] = ""   # e.g., "part-time, no relocation, budget ₹0-10k"
    prefer_learning_mode: Optional[str] = "self-study"  # bootcamp, mentorship, self-study

class CareerMilestone(BaseModel):
    month: int
    title: str
    tasks: List[str]
    outcome_metrics: Optional[Dict[str, str]] = None
    resources: Optional[List[str]] = None

class CareerPathOutput(BaseModel):
    overall_time_months: int
    confidence_score: float
    milestones: List[CareerMilestone]
    short_summary: str
    recommended_resources: List[str]

class CodeSecurityInput(BaseModel):
    code: str
    language: Optional[str] = "auto"

class VulnerabilityItem(BaseModel):
    issue: str
    severity: str
    explanation: str
    line_numbers: Optional[List[int]] = None
    fix_suggestion: Optional[str] = None

class CodeSecurityOutput(BaseModel):
    vulnerabilities: List[VulnerabilityItem]
    risk_score: float
    summary: str
    evidence_ids: List[str]
    evidence_snippets: List[Dict[str, str]]

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

class UMLRequest(BaseModel):
    description: str
    uml_type: Optional[str] = "auto"  
    # auto, class, sequence, usecase, flow, erd

class UMLResponse(BaseModel):
    uml_type: str
    mermaid_diagram: str
    explanation: str

class LearningFlowInput(BaseModel):
    topic: str
    experienceLevel: Optional[str] = "beginner"  # beginner, intermediate, advanced
    weeklyHours: Optional[str] = "5-10"  # "1-5", "5-10", "10-20", "20+"

class LearningPhase(BaseModel):
    name: str
    duration: str
    description: str
    keyTopics: List[str]

class YouTubeChannel(BaseModel):
    name: str
    url: str
    focus: str
    recommendedPlaylists: Optional[List[str]] = []

class ProjectItem(BaseModel):
    name: str
    description: str
    difficulty: str  # beginner, intermediate, advanced
    estimatedHours: int

class LearningResources(BaseModel):
    books: List[str]
    websites: List[str]
    communities: List[str]

class LearningFlowOutput(BaseModel):
    phases: List[LearningPhase]
    mermaidDiagram: str
    youtubeChannels: List[YouTubeChannel]
    projects: List[ProjectItem]
    timeline: str
    prerequisites: List[str]
    resources: LearningResources
    evidence_ids: List[str]  # RAG evidence for hackathon
    evidence_snippets: List[Dict[str, str]]  # RAG evidence snippets

class RejectionDetectorInput(BaseModel):
    resume: Optional[str] = ""
    githubUrl: Optional[str] = ""
    skills: Optional[str] = ""
    jobDescription: Optional[str] = ""
    jobDescriptionUrl: Optional[str] = ""
    inputType: Optional[str] = "text"  # text | url
    experienceYears: Optional[float] = 0.0
    currentRole: Optional[str] = ""

class RejectionReason(BaseModel):
    category: str  # "skills", "experience", "domain", "github", "resume", "soft_skills"
    severity: str  # "critical", "major", "minor"
    reason: str
    evidence: str
    impact_score: int  # 1-10, how likely this causes rejection

class ImprovementAction(BaseModel):
    action: str
    priority: str
    timeframe: str
    difficulty: str
    description: str

class RejectionDetectorOutput(BaseModel):
    overall_rejection_probability: int  # 0-100
    rejection_reasons: List[RejectionReason]
    improvement_roadmap: List[ImprovementAction]
    strengths: List[str]
    quick_wins: List[str]
    long_term_goals: List[str]
    evidence_ids: List[str]
    evidence_snippets: List[Dict[str, str]]