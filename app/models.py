from pydantic import BaseModel, Field
from typing import Optional


# ---------------------------------------------------------------------------
# Five-Pillar Assessment Schemas
# ---------------------------------------------------------------------------
# The five pillars used to assess a data / AI initiative are:
#   1. Strategy & Leadership
#   2. Data Management & Quality
#   3. Technology & Architecture
#   4. Analytics & Insights
#   5. Governance & Compliance

class PillarScore(BaseModel):
    score: int = Field(..., ge=0, le=10, description="Score from 0 to 10")
    notes: Optional[str] = Field(None, description="Optional notes for this pillar")


class AssessmentRequest(BaseModel):
    organisation: str = Field(..., description="Name of the organisation being assessed")
    document_url: Optional[str] = Field(
        None, description="Optional URL or GCS path to a PDF document for analysis"
    )
    strategy_and_leadership: PillarScore = Field(
        ..., description="Pillar 1 – Strategy & Leadership"
    )
    data_management_and_quality: PillarScore = Field(
        ..., description="Pillar 2 – Data Management & Quality"
    )
    technology_and_architecture: PillarScore = Field(
        ..., description="Pillar 3 – Technology & Architecture"
    )
    analytics_and_insights: PillarScore = Field(
        ..., description="Pillar 4 – Analytics & Insights"
    )
    governance_and_compliance: PillarScore = Field(
        ..., description="Pillar 5 – Governance & Compliance"
    )


class PillarResult(BaseModel):
    score: int
    notes: Optional[str]
    recommendation: str


class AssessmentResponse(BaseModel):
    organisation: str
    overall_score: float = Field(..., description="Average score across all five pillars")
    strategy_and_leadership: PillarResult
    data_management_and_quality: PillarResult
    technology_and_architecture: PillarResult
    analytics_and_insights: PillarResult
    governance_and_compliance: PillarResult
    summary: str = Field(..., description="AI-generated executive summary (populated by Vertex AI)")
