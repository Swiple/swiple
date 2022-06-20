from app.api.api_v1.endpoints import scheduler
from fastapi import APIRouter

router = APIRouter()
router.include_router(scheduler.router, prefix="/schedules", tags=["Scheduler"])