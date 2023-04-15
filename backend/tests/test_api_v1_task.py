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
        task_id = CELERY_TASKS['postgres_table_products'].result.task_id
        response = await test_client.get(f"/api/v1/tasks/{task_id}")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()

        assert json == {
            'date_done': '2023-03-26T17:30:56.259829',
            'kwargs': {
                'dataset_id': '5b65eae9-600e-4933-9bad-78477e0ab98e'
            },
            'name': 'validation.run',
            'result': None,
            'retries': 0,
            'status': 'SUCCESS',
            'task_id': 'c4690c54-ac50-4eaf-8a3f-104f0aef7ce7'
        }

    @pytest.mark.user
    async def test_get_pending_task(self, test_client: httpx.AsyncClient):
        task_id = 'unknown-task-id'
        response = await test_client.get(f"/api/v1/tasks/{task_id}")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()

        assert json == {
            'date_done': None,
            'kwargs': None,
            'name': None,
            'result': None,
            'retries': None,
            'status': 'PENDING',
            'task_id': 'unknown-task-id',
        }

    @pytest.mark.user
    async def test_failed_task(self, test_client: httpx.AsyncClient):
        task_id = CELERY_TASKS['postgres_view_orders'].result.task_id
        response = await test_client.get(f"/api/v1/tasks/{task_id}")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()

        assert json == {
            'date_done': '2023-03-26T15:42:16.080941',
            'kwargs': {
                'dataset_id': '4b252091-6d0d-4beb-9552-3764cfe8cbae',
            },
            'name': 'validation.run',
            'result': {
                'exc_message': [
                    'Cannot initialize datasource demo, error: The '
                    'given datasource could not be retrieved from the '
                    'DataContext; please confirm that your '
                    'configuration is accurate.'
                ],
                'exc_module': 'great_expectations.exceptions.exceptions',
                'exc_type': 'DatasourceError',
            },
            'retries': 0,
            'status': 'FAILURE',
            'task_id': 'a9cadbea-3676-44b0-be2b-26ea60267f50',
        }
