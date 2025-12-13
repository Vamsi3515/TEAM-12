from pydantic import BaseModel
from typing import List, Dict

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