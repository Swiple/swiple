from app.api.api_v1.endpoints import health, scheduler
from fastapi import APIRouter

router = APIRouter()
router.include_router(health.router, tags=["Health"])
router.include_router(scheduler.router, prefix="/schedules", tags=["Schedules"])
