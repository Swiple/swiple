from unittest.mock import MagicMock
import httpx
import pytest
from fastapi import status
from opensearchpy import OpenSearch, RequestError
from pytest_mock import MockerFixture
import requests

from app.core.runner import Runner
from app.core.sample import GetSampleException
from app.models.dataset import Sample
from app.repositories.dataset import DatasetRepository
from tests.data import DATASETS, DATASOURCES, create_validation_object


@pytest.fixture
def dataset_repository(opensearch_client: OpenSearch):
    return DatasetRepository(opensearch_client)


@pytest.fixture
def get_dataset_sample_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("app.api.api_v1.endpoints.dataset.get_dataset_sample")


@pytest.fixture
def runner_mock(mocker: MockerFixture) -> MagicMock:
    class_mock = mocker.patch("app.core.runner.Runner", spec=Runner)
    instance_mock = class_mock.return_value
    return instance_mock


@pytest.mark.asyncio
class TestGetJSONSchema:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/datasets/json-schema")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/datasets/json-schema")

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json["title"] == "Dataset"


@pytest.mark.asyncio
class TestListDatasets:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/datasets/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_invalid_sort_by_key(
        self,
        mocker: MockerFixture,
        test_client: httpx.AsyncClient,
        opensearch_client: OpenSearch,
    ):
        # Mock the error manually
        # The mock OpenSearch client doesn't seem to check sort keys
        mocker.patch.object(opensearch_client, "search", side_effect=RequestError)

        response = await test_client.get(
            "/api/v1/datasets/", params={"sort_by_key": "invalid_key"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        json = response.json()
        assert json["detail"] == "invalid sort_by_key"

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/datasets/")

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json == [
            {
                "create_date": "2022-10-04 13:37:00.000000+00:00",
                "modified_date": "2022-10-04 13:37:00.000000+00:00",
                "key": "5b65eae9-600e-4933-9bad-78477e0ab98e",
                "datasource_id": "50a58a0b-89e8-4d6f-8b65-6ea328b2cad2",
                "datasource_name": "postgres",
                "database": "postgres",
                "connector_type": "RuntimeDataConnector",
                "dataset_name": "postgres_table_products",
                "description": None,
                "runtime_parameters": {"schema": "products", "query": None},
                "engine": "PostgreSQL",
                "sample": None,
                "created_by": "admin@email.com",
            },
            {
                "create_date": "2022-10-04 13:37:00.000000+00:00",
                "modified_date": "2022-10-04 13:37:00.000000+00:00",
                "key": "4b252091-6d0d-4beb-9552-3764cfe8cbae",
                "datasource_id": "50a58a0b-89e8-4d6f-8b65-6ea328b2cad2",
                "datasource_name": "postgres",
                "database": "postgres",
                "connector_type": "RuntimeDataConnector",
                "dataset_name": "postgres_table_orders",
                "description": None,
                "runtime_parameters": {"schema": "orders", "query": None},
                "engine": "PostgreSQL",
                "sample": None,
                "created_by": "admin@email.com",
            },
            {
                "create_date": "2022-10-04 13:37:00.000000+00:00",
                "modified_date": "2022-10-04 13:37:00.000000+00:00",
                "key": "5b6adc59-d92d-4b75-9d7e-7e1e6f4392a7",
                "datasource_id": "dd19ce80-e020-4a63-9f52-9d0950558df6",
                "datasource_name": "mysql",
                "database": "mysql",
                "connector_type": "RuntimeDataConnector",
                "dataset_name": "mysql_table_products",
                "description": None,
                "runtime_parameters": {"schema": "products", "query": None},
                "engine": "MySQL",
                "sample": None,
                "created_by": "admin@email.com",
            },
        ]

    @pytest.mark.user
    async def test_filter_datasource_id(self, test_client: httpx.AsyncClient):
        datasource_id = DATASOURCES["postgres"].key
        response = await test_client.get(
            "/api/v1/datasets/", params={"datasource_id": datasource_id}
        )

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert len(json) == 2
        for dataset in json:
            assert dataset["datasource_id"] == datasource_id


@pytest.mark.asyncio
class TestGetDataset:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.get(
            "/api/v1/datasets/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.get(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}"
        )

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json == {
            "create_date": "2022-10-04 13:37:00.000000+00:00",
            "modified_date": "2022-10-04 13:37:00.000000+00:00",
            "key": "5b65eae9-600e-4933-9bad-78477e0ab98e",
            "datasource_id": "50a58a0b-89e8-4d6f-8b65-6ea328b2cad2",
            "datasource_name": "postgres",
            "database": "postgres",
            "connector_type": "RuntimeDataConnector",
            "dataset_name": "postgres_table_products",
            "description": None,
            "runtime_parameters": {"schema": "products", "query": None},
            "engine": "PostgreSQL",
            "sample": None,
            "created_by": "admin@email.com",
        }


@pytest.mark.asyncio
class TestCreateDataset:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.post("/api/v1/datasets/", json={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_already_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            "/api/v1/datasets/",
            json={
                "datasource_id": DATASOURCES["postgres"].key,
                "datasource_name": DATASOURCES["postgres"].datasource_name,
                "database": DATASOURCES["postgres"].database,
                "dataset_name": "postgres_table_products",
                "runtime_parameters": {"schema": "products"},
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        json = response.json()
        assert (
            json["detail"]
            == "dataset 'postgres.products.postgres_table_products' already exists"
        )

    @pytest.mark.user
    async def test_get_sample_exception(
        self, get_dataset_sample_mock: MagicMock, test_client: httpx.AsyncClient
    ):
        get_dataset_sample_mock.side_effect = GetSampleException("get_sample_error")

        response = await test_client.post(
            "/api/v1/datasets/",
            json={
                "datasource_id": DATASOURCES["postgres"].key,
                "datasource_name": DATASOURCES["postgres"].datasource_name,
                "database": DATASOURCES["postgres"].database,
                "dataset_name": "postgres_table_users",
                "runtime_parameters": {"schema": "users"},
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        json = response.json()
        json["detail"] == "get_sample_error"

    @pytest.mark.user
    async def test_allowed(
        self, get_dataset_sample_mock: MagicMock, test_client: httpx.AsyncClient
    ):
        get_dataset_sample_mock.return_value = Sample(columns=[], rows=[])

        response = await test_client.post(
            "/api/v1/datasets/",
            json={
                "datasource_id": DATASOURCES["postgres"].key,
                "datasource_name": DATASOURCES["postgres"].datasource_name,
                "database": DATASOURCES["postgres"].database,
                "dataset_name": "postgres_table_users",
                "runtime_parameters": {"schema": "users"},
            },
        )

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json["engine"] == "PostgreSQL"
        assert json["created_by"] == "admin@email.com"
        assert json["create_date"] is not None
        assert json["modified_date"] is not None
        assert json["sample"] == {"columns": [], "rows": []}


@pytest.mark.asyncio
class TestUpdateDataset:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}", json={}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            "/api/v1/datasets/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0",
            json={
                "datasource_id": DATASOURCES["postgres"].key,
                "datasource_name": DATASOURCES["postgres"].datasource_name,
                "database": DATASOURCES["postgres"].database,
                "dataset_name": "postgres_table_products",
                "runtime_parameters": {"schema": "products"},
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_update_datasource(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}",
            json={
                "datasource_id": DATASOURCES["mysql"].key,
                "datasource_name": DATASOURCES["postgres"].datasource_name,
                "database": DATASOURCES["postgres"].database,
                "dataset_name": "postgres_table_products",
                "runtime_parameters": {"schema": "products"},
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        json = response.json()
        json["detail"] == "updates to dataset datasource_id are not supported"

    @pytest.mark.user
    async def test_conflicting_name(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}",
            json={
                "datasource_id": DATASOURCES["postgres"].key,
                "datasource_name": DATASOURCES["postgres"].datasource_name,
                "database": DATASOURCES["postgres"].database,
                "dataset_name": DATASETS["postgres_table_orders"].dataset_name,
                "runtime_parameters": {"schema": "orders"},
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        json = response.json()
        assert (
            json["detail"]
            == "dataset 'postgres.orders.postgres_table_orders' already exists"
        )

    @pytest.mark.user
    async def test_allowed(
        self, test_client: httpx.AsyncClient, dataset_repository: DatasetRepository
    ):
        response = await test_client.put(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}",
            json={
                "datasource_id": DATASOURCES["postgres"].key,
                "datasource_name": DATASOURCES["postgres"].datasource_name,
                "database": DATASOURCES["postgres"].database,
                "dataset_name": "updated_name",
                "runtime_parameters": {"schema": "products_bis"},
            },
        )

        assert response.status_code == status.HTTP_200_OK

        updated_dataset = dataset_repository.get(
            DATASETS["postgres_table_products"].key
        )

        assert updated_dataset.dataset_name == "updated_name"
        assert (
            updated_dataset.create_date
            == DATASETS["postgres_table_products"].create_date
        )
        assert (
            updated_dataset.modified_date
            != DATASETS["postgres_table_products"].modified_date
        )


@pytest.mark.asyncio
class TestDeleteDataset:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.delete(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.delete(
            "/api/v1/datasets/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_allowed(self, mocker: MockerFixture, test_client: httpx.AsyncClient):
        # Mock requests.delete request
        # This shall be removed when we delete the schedules without an HTTP request to our own API
        mocker.patch.object(requests, "delete", return_value=None)

        response = await test_client.delete(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}"
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
class TestCreateSample:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.post("/api/v1/datasets/sample", json={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing_datasource(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            "/api/v1/datasets/sample",
            json={
                "datasource_id": "5ecf8e33-2c19-4ed7-a11a-def2cd494ef0",
                "datasource_name": "not_existing_datasource",
                "database": "postgres",
                "dataset_name": "postgres_table",
                "runtime_parameters": {"schema": "products"},
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_get_sample_exception(
        self, get_dataset_sample_mock: MagicMock, test_client: httpx.AsyncClient
    ):
        get_dataset_sample_mock.side_effect = GetSampleException("get_sample_error")

        response = await test_client.post(
            "/api/v1/datasets/sample",
            json={
                "datasource_id": DATASOURCES["postgres"].key,
                "datasource_name": DATASOURCES["postgres"].datasource_name,
                "database": DATASOURCES["postgres"].database,
                "dataset_name": "postgres_table_users",
                "runtime_parameters": {"schema": "users"},
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        json = response.json()
        json["detail"] == "get_sample_error"

    @pytest.mark.user
    async def test_allowed(
        self, get_dataset_sample_mock: MagicMock, test_client: httpx.AsyncClient
    ):
        get_dataset_sample_mock.return_value = Sample(columns=[], rows=[])

        response = await test_client.post(
            "/api/v1/datasets/sample",
            json={
                "datasource_id": DATASOURCES["postgres"].key,
                "datasource_name": DATASOURCES["postgres"].datasource_name,
                "database": DATASOURCES["postgres"].database,
                "dataset_name": "postgres_table_users",
                "runtime_parameters": {"schema": "users"},
            },
        )

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json == {"columns": [], "rows": []}


@pytest.mark.asyncio
class TestUpdateSample:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}/sample",
            json={},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/datasets/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0/sample", json={}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_get_sample_exception(
        self, get_dataset_sample_mock: MagicMock, test_client: httpx.AsyncClient
    ):
        get_dataset_sample_mock.side_effect = GetSampleException("get_sample_error")

        response = await test_client.put(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}/sample",
            json={},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        json = response.json()
        json["detail"] == "get_sample_error"

    @pytest.mark.user
    async def test_allowed(
        self,
        get_dataset_sample_mock: MagicMock,
        test_client: httpx.AsyncClient,
        dataset_repository: DatasetRepository,
    ):
        get_dataset_sample_mock.return_value = Sample(columns=[], rows=[])

        response = await test_client.put(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}/sample",
            json={},
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json["key"] == DATASETS["postgres_table_products"].key

        updated_dataset = dataset_repository.get(
            DATASETS["postgres_table_products"].key
        )

        assert updated_dataset.sample == Sample(columns=[], rows=[])
        assert (
            updated_dataset.create_date
            == DATASETS["postgres_table_products"].create_date
        )
        assert (
            updated_dataset.modified_date
            != DATASETS["postgres_table_products"].modified_date
        )


@pytest.mark.asyncio
class TestValidateDataset:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}/validate",
            json={},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            f"/api/v1/datasets/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0/validate", json={}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_allowed(
        self, runner_mock: MagicMock, test_client: httpx.AsyncClient
    ):
        validation = create_validation_object(
            DATASOURCES["postgres"].key, DATASETS["postgres_table_products"].key
        )
        runner_mock.validate.return_value = validation

        response = await test_client.post(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}/validate",
            json={},
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == validation.dict()


@pytest.mark.asyncio
class TestCreateSuggestions:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}/suggest",
            json={},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            f"/api/v1/datasets/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0/suggest", json={}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_allowed(
        self, runner_mock: MagicMock, test_client: httpx.AsyncClient
    ):
        runner_mock.profile.return_value = []

        response = await test_client.post(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}/suggest",
            json={},
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == []
