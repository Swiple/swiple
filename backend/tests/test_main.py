import httpx
import pytest
from fastapi import status

from app.settings import settings


@pytest.mark.asyncio
async def test_openapi(test_client: httpx.AsyncClient):
    response = await test_client.get(f"{settings.API_VERSION}/openapi.json")

    assert response.status_code == status.HTTP_200_OK
