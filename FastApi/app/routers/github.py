from fastapi import APIRouter, HTTPException
from app.models.schemas import GitHubAnalyzeInput, GitHubAnalyzeOutput
from app.core.github_agent import analyze_github_repo

router = APIRouter(prefix="", tags=["GitHub Analyzer"])  # Empty prefix, full path in route

@router.post("/analyze-github", response_model=GitHubAnalyzeOutput)
async def analyze(body: GitHubAnalyzeInput):
    return await analyze_github_repo(body.repoUrl)  # Access camelCase field