from fastapi import APIRouter
from app.models.schemas import LearningFlowInput, LearningFlowOutput
from app.core.Agents.learning_agent import generate_learning_flow

router = APIRouter(prefix="/api/learning-flow", tags=["Learning Flow Generator"])

@router.post("/generate", response_model=LearningFlowOutput)
async def create_learning_flow(body: LearningFlowInput):
    # Map frontend fields (topic, experienceLevel, weeklyHours) to agent inputs
    result = await generate_learning_flow(
        topic=body.topic,
        experience_level=body.experienceLevel,
        weekly_hours=body.weeklyHours,
    )
    return result
