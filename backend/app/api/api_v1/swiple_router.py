from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    auth,
    dataset,
    dashboard,
    datasource,
    expectation,
    runner,
    introspect,
    validation,
    suggestion,
    schedule,
)

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(datasource.router, prefix="/datasources", tags=["Data Sources"])
router.include_router(dataset.router, prefix="/datasets", tags=["Datasets"])
router.include_router(expectation.router, prefix="/expectation", tags=["Expectations"])
router.include_router(runner.router, prefix="/runner", tags=["Runner"])
router.include_router(validation.router, prefix="/validation", tags=["Validations"])
router.include_router(suggestion.router, prefix="/suggestion", tags=["Suggestions"])
router.include_router(introspect.router, prefix="/introspect", tags=["Introspect"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
router.include_router(schedule.router, prefix="/schedules", tags=["Schedule"])
