"""
WASTESENSE — FastAPI application entry point.
Member 5: Backend + ML Integration
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from backend.api.routes import router as api_router
from backend.services.ml_service import (
    MLInputError,
    MLModelUnavailableError,
    MLServiceError,
    analyze_workload,
)

app = FastAPI(
    title="WASTESENSE API",
    description="API for intelligent resource waste detection and optimization.",
    version="0.1.0",
)

# Register shared API routes.
app.include_router(api_router)


class WorkloadRequest(BaseModel):
    """Validate workload data submitted to the ML analysis endpoint."""

    model_config = ConfigDict(extra="allow")

    machine_id: str = Field(min_length=1)
    timestamp: str = Field(min_length=1)
    active_tasks: int = Field(ge=0)
    workload_type: str = "COMPUTE"
    priority: float = 1.0
    workload_duration: float = 0.0
    cpu_capacity: float = Field(gt=0)
    memory_capacity: float = Field(gt=0)
    actual_cpu: float = Field(ge=0)
    actual_memory: float = Field(ge=0)


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    return {
        "message": "WASTESENSE API is running",
        "status": "healthy",
    }


@app.get("/api/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "wastesense-backend",
    }


@app.post("/api/waste/analyze", tags=["Waste Analysis"])
async def analyze_waste(request: WorkloadRequest) -> dict:
    try:
        return analyze_workload(request.model_dump())

    except MLInputError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    except MLModelUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    except MLServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Workload analysis failed unexpectedly.",
        ) from None