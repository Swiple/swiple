from unittest.mock import patch

import httpx
import pytest
from fastapi import status

from tests.data import CELERY_TASKS
from tests.fake_opensearch import FakeOpenSearch
import app.db.client


@pytest.mark.asyncio
class TestGetTask:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        task_id = "some-task-id"
        response = await test_client.get(f"/api/v1/tasks/{task_id}")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_get_task(self, test_client: httpx.AsyncClient):
        with patch.object(app.db.client, 'client', FakeOpenSearch()):

            # Replace this with a valid task id for your testing
            task_id = CELERY_TASKS['postgres_table_products'].result.task_id
            response = await test_client.get(f"/api/v1/tasks/{task_id}")

            assert response.status_code == status.HTTP_200_OK
            json = response.json()
            # Assert the response contains the expected data
            assert json["task_id"] == task_id
