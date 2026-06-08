"""
services.py – Business logic layer.

This module is the integration point for:
  - Vertex AI (Gemini) for AI-generated assessment summaries and recommendations
  - PDF parsing / document extraction for uploaded assessment documents

All functions are stubbed out and return placeholder data until the
Vertex AI and PDF integrations are implemented.
"""
from __future__ import annotations

import vertexai
from vertexai.generative_models import GenerativeModel
import os


from app.models import (
    AssessmentRequest,
    AssessmentResponse,
    PillarResult,
)


# ---------------------------------------------------------------------------
# Recommendation helpers (stub – will call Vertex AI in a future iteration)
# ---------------------------------------------------------------------------

_PILLAR_RECOMMENDATIONS: dict[str, str] = {
    "strategy_and_leadership": (
        "Define a clear data strategy aligned with organisational goals and ensure "
        "executive sponsorship for data initiatives."
    ),
    "data_management_and_quality": (
        "Implement data governance policies, establish data quality KPIs, and adopt "
        "a master data management framework."
    ),
    "technology_and_architecture": (
        "Invest in a modern, scalable data platform and ensure interoperability "
        "between existing systems."
    ),
    "analytics_and_insights": (
        "Build self-service analytics capabilities and promote a data-driven culture "
        "across all business units."
    ),
    "governance_and_compliance": (
        "Establish clear data ownership, enforce access controls, and maintain "
        "compliance with applicable data regulations."
    ),
}


def _recommendation_for(pillar_key: str) -> str:
    return _PILLAR_RECOMMENDATIONS.get(pillar_key, "No recommendation available.")


# ---------------------------------------------------------------------------
# PDF / document extraction (stub)
# ---------------------------------------------------------------------------

async def extract_text_from_document(document_url: str) -> str:  # noqa: ARG001
    """Extract plain text from a PDF document.

    TODO: Implement using Google Cloud Document AI or a PDF parsing library
    once a document_url (GCS path or HTTPS URL) is provided.
    """
    return ""


# ---------------------------------------------------------------------------
# Vertex AI summary generation (stub)
# ---------------------------------------------------------------------------

async def generate_summary(request: AssessmentRequest, overall_score: float) -> str:
    """Generate an AI-powered executive summary using Vertex AI (Gemini)."""
    
    # In Cloud Run, GOOGLE_CLOUD_PROJECT is automatically injected. 
    # For local testing, ensure you have run `gcloud auth application-default login`
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "datai-core")
    location = "europe-west6"
    
    vertexai.init(project=project_id, location=location)
    
    # We use Gemini 1.5 Flash for high speed and low latency
    model = GenerativeModel("gemini-1.5-flash")
    
    # Construct the system context and user prompt
    prompt = f"""
    You are an expert Data & AI Management Consultant at the boutique firm 'datai'. 
    You are evaluating a potential client organisation named: {request.organisation}.
    
    They just completed a Data & AI Maturity Assessment and scored an overall {overall_score:.1f}/10.
    
    Here is the breakdown of their 5 pillars:
    1. Strategy & Leadership: {request.strategy_and_leadership.score}/10. Notes: {request.strategy_and_leadership.notes}
    2. Data Management & Quality: {request.data_management_and_quality.score}/10. Notes: {request.data_management_and_quality.notes}
    3. Technology & Architecture: {request.technology_and_architecture.score}/10. Notes: {request.technology_and_architecture.notes}
    4. Analytics & Insights: {request.analytics_and_insights.score}/10. Notes: {request.analytics_and_insights.notes}
    5. Governance & Compliance: {request.governance_and_compliance.score}/10. Notes: {request.governance_and_compliance.notes}
    
    Write a concise, professional, 2-paragraph executive summary tailored to this client. 
    The first paragraph should assess their current state. 
    The second paragraph should provide 2-3 high-level, actionable next steps to improve their capabilities.
    Do not use markdown formatting like **bolding** as this will be parsed into a PDF later.
    """
    
    try:
        # Generate the response asynchronously to keep the FastAPI server non-blocking
        response = await model.generate_content_async(prompt)
        return response.text.strip()
    except Exception as e:
        # Fallback error handling if the API fails
        return f"Assessment complete (Score: {overall_score:.1f}/10). AI summary generation temporarily unavailable. Error: {str(e)}"

# ---------------------------------------------------------------------------
# Core assessment logic
# ---------------------------------------------------------------------------

async def run_assessment(request: AssessmentRequest) -> AssessmentResponse:
    """Execute the full assessment pipeline and return a structured response."""

    pillar_keys = [
        "strategy_and_leadership",
        "data_management_and_quality",
        "technology_and_architecture",
        "analytics_and_insights",
        "governance_and_compliance",
    ]

    # Build per-pillar results
    results: dict[str, PillarResult] = {}
    scores: list[int] = []

    for key in pillar_keys:
        pillar_input = getattr(request, key)
        results[key] = PillarResult(
            score=pillar_input.score,
            notes=pillar_input.notes,
            recommendation=_recommendation_for(key),
        )
        scores.append(pillar_input.score)

    overall_score = sum(scores) / len(scores)

    # Optionally extract text from a supplied document (stub)
    if request.document_url:
        await extract_text_from_document(request.document_url)

    summary = await generate_summary(request, overall_score)

    return AssessmentResponse(
        organisation=request.organisation,
        overall_score=round(overall_score, 2),
        summary=summary,
        **results,
    )
