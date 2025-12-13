"""Router for Experience Authenticity & Skill Consistency Agent."""

from fastapi import APIRouter, HTTPException
from app.models.authenticity import (
    AuthenticityAnalysisInput,
    AuthenticityExtendedInput,
    AuthenticityExtendedOutput,
)
from app.core.authenticity_agent import analyze_authenticity

router = APIRouter(tags=["Authenticity & Skill Consistency"])


@router.post("/analyze-authenticity", response_model=AuthenticityExtendedOutput)
async def analyze_skill_consistency(input_data: AuthenticityExtendedInput | AuthenticityAnalysisInput) -> AuthenticityExtendedOutput:
    """
    Experience Authenticity & Skill Consistency Agent
    
    Analyzes the alignment between resume claims and observable evidence (GitHub, LeetCode)
    to generate confidence and risk signals about employability readiness.
    
    This is a SUPPORTIVE decision-support system, not a fraud detector.
    
    Input:
    - resume: Parsed resume data (skills, experience, projects, education)
    - github (optional): GitHub profile analysis (languages, repos, commits, README quality)
    - leetcode (optional): LeetCode stats (problems solved, difficulty distribution, activity)
    - additional_context (optional): Any other relevant information
    
    Output (Strict JSON):
    - confidence_level: "High" | "Medium" | "Low"
    - authenticity_score: 0-100 (based on evidence comprehensiveness, not honesty)
    - strong_evidence: List of supported skills and positive signals
    - risk_indicators: List of weak or missing evidence areas (framed as opportunities)
    - overall_assessment: Short, neutral, encouraging explanation
    - improvement_suggestions: Actionable steps to strengthen evidence
    - skill_alignments: Detailed skill-by-skill analysis
    
    Key Principles:
    ✓ Supportive and candidate-friendly tone
    ✓ Does NOT assume missing evidence = dishonesty
    ✓ Does NOT penalize for lack of GitHub/LeetCode
    ✓ Highlights both strengths AND opportunities
    ✓ Neutral, professional, non-accusatory language
    """
    try:
        return await analyze_authenticity(input_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
