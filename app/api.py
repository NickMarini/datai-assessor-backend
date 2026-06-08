from fastapi import APIRouter
from app.models import AssessmentRequest, AssessmentResponse
from app.services import run_assessment

router = APIRouter(prefix="/api/v1", tags=["assessment"])


@router.post("/assess", response_model=AssessmentResponse, summary="Run a five-pillar assessment")
async def assess(request: AssessmentRequest) -> AssessmentResponse:
    """Submit an assessment request and receive scores, recommendations, and an AI summary."""
    return await run_assessment(request)
