from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

app = FastAPI(
    title="datai Assessor API",
    description="Backend API for running five-pillar data maturity assessments.",
    version="0.1.0",
)

# Configure CORS for Firebase frontend
origins = [
    "https://datai.ch",
    "https://dev.datai.ch",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods including POST and OPTIONS
    allow_headers=["*"], # Allows all headers
)

app.include_router(router)

@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Basic liveness probe."""
    return {"status": "ok"}