import httpx
import pytest
from fastapi import status


@pytest.mark.asyncio
class TestGetJSONSchema:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/datasources/json-schema")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/datasources/json-schema")

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert len(json) == 6
