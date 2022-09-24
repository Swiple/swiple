from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.api.api_v1 import auth_router
from app.settings import settings
from app.db.client import client, async_client
import app.constants as c
from app.core.schedulers.scheduler import scheduler
from app.api import exception_handlers

app = FastAPI(
    openapi_url=f"{settings.API_VERSION}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(auth_router.router, prefix=settings.API_VERSION)

if settings.APP == c.APP_SWIPLE_API:
    from app.api.api_v1 import swiple_router
    app.include_router(swiple_router.router, prefix=settings.API_VERSION)

if settings.APP == c.APP_SCHEDULER:
    from app.api.api_v1 import scheduler_router
    app.include_router(scheduler_router.router, prefix=settings.API_VERSION)

exception_handlers.add(app)


@app.router.on_event("startup")
async def startup():
    if settings.APP == c.APP_SCHEDULER:
        scheduler.start()


@app.router.on_event("shutdown")
async def shutdown():
    await async_client.close()
    client.close()

    if settings.APP == c.APP_SCHEDULER:
        scheduler.shutdown()
