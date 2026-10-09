from fastapi import FastAPI

from backend.api.routes.health import router as health_router
from backend.api.routes.machines import router as machines_router
from backend.core.config import API_V1_PREFIX, APP_NAME, APP_VERSION
from backend.api.routes.workloads import router as workloads_router
from backend.api.routes.waste_events import router as waste_events_router
from backend.api.routes.measurements import router as measurements_router
from backend.api.routes.alerts import router as alerts_router
from backend.api.routes.savings import router as savings_router
from backend.api.routes.replay_results import (
    router as replay_results_router,
)

from backend.api.routes.recommendation import (
    router as recommendations_router,
)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Backend API for the WASTESENSE resource waste detection platform.",
)

app.include_router(health_router, prefix=API_V1_PREFIX)
app.include_router(machines_router, prefix=API_V1_PREFIX)
app.include_router(workloads_router, prefix=API_V1_PREFIX)

app.include_router(measurements_router, prefix=API_V1_PREFIX)
app.include_router(
    waste_events_router,
    prefix=API_V1_PREFIX,
)
app.include_router(
    alerts_router,
    prefix=API_V1_PREFIX,
)

app.include_router(
    savings_router,
    prefix=API_V1_PREFIX,
)

app.include_router(
    replay_results_router,
    prefix=API_V1_PREFIX,
)

app.include_router(
    recommendations_router,
    prefix=API_V1_PREFIX,
)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }
