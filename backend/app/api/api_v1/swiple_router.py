from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    auth,
    dataset,
    datasource,
    expectation,
    introspect,
    validation,
    schedule,
    metrics,
)

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(datasource.router, prefix="/datasources", tags=["Data Sources"])
router.include_router(dataset.router, prefix="/datasets", tags=["Datasets"])
router.include_router(expectation.router, prefix="/expectations", tags=["Expectations"])
router.include_router(validation.router, prefix="/validations", tags=["Validations"])
router.include_router(introspect.router, prefix="/introspect", tags=["Introspect"])
router.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
router.include_router(schedule.router, prefix="/schedules", tags=["Schedule"])
