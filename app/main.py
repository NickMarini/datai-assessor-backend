from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="datai Assessor API",
    description="Backend API for running five-pillar data maturity assessments.",
    version="0.1.0",
)

app.include_router(router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Basic liveness probe."""
    return {"status": "ok"}
