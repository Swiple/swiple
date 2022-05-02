from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.api.api_v1.api import router
from app.config.settings import settings
from app.db.client import client, async_client

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


@router.on_event("startup")
async def startup():
    pass


@router.on_event("shutdown")
async def shutdown():
    await async_client.close()
    client.close()

app.include_router(router, prefix=settings.API_VERSION)
