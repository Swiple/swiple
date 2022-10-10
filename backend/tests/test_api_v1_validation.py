import httpx
import pytest
from fastapi import status
from opensearchpy import OpenSearch
from pytest_mock import MockerFixture

from app.main import app
from app.repositories.validation import ValidationRepository, get_validation_repository
from tests.data import DATASETS, DATASOURCES, VALIDATIONS


@pytest.fixture(autouse=True)
def validation_repository(mocker: MockerFixture, opensearch_client: OpenSearch):
    repository = ValidationRepository(opensearch_client)

    # FakeOpenSearch is not able to handle complex queries, so we fake them
    mocker.patch.object(
        repository, "query_by_filter", return_value=list(VALIDATIONS.values())
    )
    mocker.patch.object(
        repository,
        "statistics",
        return_value={
            "aggregations": {
                "31_day": {
                    "success_counts": {"value": 90},
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [],
                },
                "7_day": {
                    "success_counts": {"value": 90},
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [],
                },
                "1_day": {
                    "success_counts": {"value": 90},
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [],
                },
                "validation_counts": {
                    "success_counts": {"value": 90},
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [],
                },
            }
        },
    )

    app.dependency_overrides[get_validation_repository] = lambda: repository

    return repository


@pytest.mark.asyncio
class TestListValidations:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/validations/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_datasource_and_dataset_not_provided(
        self, test_client: httpx.AsyncClient
    ):
        response = await test_client.get("/api/v1/validations/")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        json = response.json()
        assert json["detail"] == "Expected either datasource_id or dataset_id"

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.get(
            "/api/v1/validations/",
            params={"datasource_id": DATASOURCES["postgres"].key},
        )

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json == [
            {
                "meta": {
                    "great_expectations_version": "1.0.0",
                    "expectation_suite_name": "expectation_suite_name",
                    "run_id": {
                        "run_time": "run_time",
                        "run_name": "run_name",
                    },
                    "batch_spec": {},
                    "batch_markers": {},
                    "active_batch_definition": {
                        "datasource_name": "datasource_name",
                        "data_connector_name": "data_connector_name",
                        "data_asset_name": "data_asset_name",
                        "batch_identifiers": {},
                    },
                    "validation_time": "validation_time",
                    "checkpoint_name": None,
                    "datasource_id": "50a58a0b-89e8-4d6f-8b65-6ea328b2cad2",
                    "dataset_id": "5b65eae9-600e-4933-9bad-78477e0ab98e",
                },
                "statistics": {
                    "evaluated_expectations": 100,
                    "successful_expectations": 90,
                    "unsuccessful_expectations": 10,
                    "success_percent": 0.1,
                },
                "results": [],
                "success": False,
                "evaluation_parameters": {},
            },
            {
                "meta": {
                    "great_expectations_version": "1.0.0",
                    "expectation_suite_name": "expectation_suite_name",
                    "run_id": {
                        "run_time": "run_time",
                        "run_name": "run_name",
                    },
                    "batch_spec": {},
                    "batch_markers": {},
                    "active_batch_definition": {
                        "datasource_name": "datasource_name",
                        "data_connector_name": "data_connector_name",
                        "data_asset_name": "data_asset_name",
                        "batch_identifiers": {},
                    },
                    "validation_time": "validation_time",
                    "checkpoint_name": None,
                    "datasource_id": "50a58a0b-89e8-4d6f-8b65-6ea328b2cad2",
                    "dataset_id": "4b252091-6d0d-4beb-9552-3764cfe8cbae",
                },
                "statistics": {
                    "evaluated_expectations": 100,
                    "successful_expectations": 90,
                    "unsuccessful_expectations": 10,
                    "success_percent": 0.1,
                },
                "results": [],
                "success": False,
                "evaluation_parameters": {},
            },
            {
                "meta": {
                    "great_expectations_version": "1.0.0",
                    "expectation_suite_name": "expectation_suite_name",
                    "run_id": {
                        "run_time": "run_time",
                        "run_name": "run_name",
                    },
                    "batch_spec": {},
                    "batch_markers": {},
                    "active_batch_definition": {
                        "datasource_name": "datasource_name",
                        "data_connector_name": "data_connector_name",
                        "data_asset_name": "data_asset_name",
                        "batch_identifiers": {},
                    },
                    "validation_time": "validation_time",
                    "checkpoint_name": None,
                    "datasource_id": "dd19ce80-e020-4a63-9f52-9d0950558df6",
                    "dataset_id": "5b6adc59-d92d-4b75-9d7e-7e1e6f4392a7",
                },
                "statistics": {
                    "evaluated_expectations": 100,
                    "successful_expectations": 90,
                    "unsuccessful_expectations": 10,
                    "success_percent": 0.1,
                },
                "results": [],
                "success": False,
                "evaluation_parameters": {},
            },
        ]


@pytest.mark.asyncio
class TestListStatistics:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/validations/statistics")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_missing_dataset_id(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/validations/statistics")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.get(
            "/api/v1/validations/statistics",
            params={"dataset_id": DATASETS["postgres_table_products"].key},
        )

        assert response.status_code == status.HTTP_200_OK
