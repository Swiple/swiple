import httpx
import pytest
from fastapi import status


@pytest.mark.asyncio
class TestGetHealth:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/health")

        assert response.status_code == status.HTTP_200_OK
