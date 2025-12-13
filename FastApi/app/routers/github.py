from fastapi import APIRouter, HTTPException
from app.models.schemas import GitHubAnalyzeInput, GitHubAnalyzeOutput

router = APIRouter(prefix="", tags=["GitHub Analyzer"])  # Empty prefix, full path in route

@router.post("/analyze-github", response_model=GitHubAnalyzeOutput)
async def analyze(body: GitHubAnalyzeInput):
    return await analyze_github_repo(body.repoUrl)  # Access camelCase field