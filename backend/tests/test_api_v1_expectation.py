from typing import Any
import httpx
import pytest
from fastapi import status
from opensearchpy import OpenSearch
from app.repositories.base import NotFoundError

from app.repositories.expectation import ExpectationRepository
from tests.data import DATASETS, DATASOURCES, EXPECTATIONS


@pytest.fixture
def expectation_repository(opensearch_client: OpenSearch):
    return ExpectationRepository(opensearch_client)


@pytest.mark.asyncio
class TestGetJSONSchema:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/expectations/json-schema")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/expectations/json-schema")

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert len(json) == 31


@pytest.mark.asyncio
class TestListSupportedExpectations:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/expectations/supported")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/expectations/supported")

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert len(json["supported_expectations"]) == 31
        assert len(json["unsupported_expectations"]) == 32


@pytest.mark.asyncio
class TestListExpectations:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/expectations/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/expectations/")

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json == [
            {
                "create_date": "2022-10-04 13:37:00.000000+00:00",
                "modified_date": "2022-10-04 13:37:00.000000+00:00",
                "key": "0815f53c-a3da-42e5-b010-560d9486830e",
                "dataset_id": "5b65eae9-600e-4933-9bad-78477e0ab98e",
                "datasource_id": "50a58a0b-89e8-4d6f-8b65-6ea328b2cad2",
                "expectation_type": "expect_column_to_exist",
                "result_type": "expectation",
                "kwargs": {
                    "column": "product_name",
                    "column_index": None,
                    "result_format": "SUMMARY",
                    "include_config": True,
                    "catch_exceptions": True,
                },
                "enabled": True,
                "suggested": False,
                "meta": None,
                "validations": [],
                "documentation": 'Expect column "product_name" to exist.',
            },
            {
                "create_date": "2022-10-04 13:37:00.000000+00:00",
                "modified_date": "2022-10-04 13:37:00.000000+00:00",
                "key": "2292afa9-01bf-4f5a-9398-e5ed5a9f7995",
                "dataset_id": "4b252091-6d0d-4beb-9552-3764cfe8cbae",
                "datasource_id": "50a58a0b-89e8-4d6f-8b65-6ea328b2cad2",
                "expectation_type": "expect_column_to_exist",
                "result_type": "expectation",
                "kwargs": {
                    "column": "order_name",
                    "column_index": None,
                    "result_format": "SUMMARY",
                    "include_config": True,
                    "catch_exceptions": True,
                },
                "enabled": True,
                "suggested": False,
                "meta": None,
                "validations": [],
                "documentation": 'Expect column "order_name" to exist.',
            },
            {
                "create_date": "2022-10-04 13:37:00.000000+00:00",
                "modified_date": "2022-10-04 13:37:00.000000+00:00",
                "key": "be3fb099-8bde-430c-b155-0488ef766e0f",
                "dataset_id": "5b6adc59-d92d-4b75-9d7e-7e1e6f4392a7",
                "datasource_id": "dd19ce80-e020-4a63-9f52-9d0950558df6",
                "expectation_type": "expect_column_to_exist",
                "result_type": "expectation",
                "kwargs": {
                    "column": "product_name",
                    "column_index": None,
                    "result_format": "SUMMARY",
                    "include_config": True,
                    "catch_exceptions": True,
                },
                "enabled": True,
                "suggested": False,
                "meta": None,
                "validations": [],
                "documentation": 'Expect column "product_name" to exist.',
            },
        ]

    @pytest.mark.user
    @pytest.mark.parametrize(
        "params,nb_results",
        [
            pytest.param(
                {"datasource_id": DATASOURCES["postgres"].key},
                2,
                id="Filter by datasource_id",
            ),
            pytest.param(
                {"dataset_id": DATASETS["postgres_table_products"].key},
                1,
                id="Filter by dataset_id",
            ),
            pytest.param(
                {"suggested": True},
                0,
                id="Filter by suggested=True",
            ),
            pytest.param(
                {"enabled": False},
                1,
                id="Filter by enabled=False",
            ),
        ],
    )
    async def test_filters(
        self, params: dict[str, Any], nb_results: int, test_client: httpx.AsyncClient
    ):
        datasource_id = DATASOURCES["postgres"].key
        response = await test_client.get("/api/v1/expectations/", params=params)

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert len(json) == nb_results


@pytest.mark.asyncio
class TestGetExpectation:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_expect_column_to_exist'].key}"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.get(
            "/api/v1/expectations/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.get(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_expect_column_to_exist'].key}"
        )

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json == {
            "create_date": "2022-10-04 13:37:00.000000+00:00",
            "modified_date": "2022-10-04 13:37:00.000000+00:00",
            "key": "0815f53c-a3da-42e5-b010-560d9486830e",
            "dataset_id": "5b65eae9-600e-4933-9bad-78477e0ab98e",
            "datasource_id": "50a58a0b-89e8-4d6f-8b65-6ea328b2cad2",
            "expectation_type": "expect_column_to_exist",
            "result_type": "expectation",
            "kwargs": {
                "column": "product_name",
                "column_index": None,
                "result_format": "SUMMARY",
                "include_config": True,
                "catch_exceptions": True,
            },
            "enabled": True,
            "suggested": False,
            "meta": None,
            "validations": [],
            "documentation": 'Expect column "product_name" to exist.',
        }


@pytest.mark.asyncio
class TestCreateExpectation:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.post("/api/v1/expectations/", json={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing_datasource(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            "/api/v1/expectations/",
            json={
                "dataset_id": DATASETS["postgres_table_products"].key,
                "datasource_id": "5ecf8e33-2c19-4ed7-a11a-def2cd494ef0",
                "expectation_type": "expect_column_to_exist",
                "kwargs": {"column": "product_name"},
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_not_existing_dataset(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            "/api/v1/expectations/",
            json={
                "dataset_id": "5ecf8e33-2c19-4ed7-a11a-def2cd494ef0",
                "datasource_id": DATASOURCES["postgres"].key,
                "expectation_type": "expect_column_to_exist",
                "kwargs": {"column": "product_name"},
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_datasource_not_matching_dataset(
        self, test_client: httpx.AsyncClient
    ):
        response = await test_client.post(
            "/api/v1/expectations/",
            json={
                "dataset_id": DATASETS["mysql_table_products"].key,
                "datasource_id": DATASOURCES["postgres"].key,
                "expectation_type": "expect_column_to_exist",
                "kwargs": {"column": "product_name"},
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        json = response.json()
        json[
            "detail"
        ] == "expectation datasource_id does not match dataset datasource_id"

    @pytest.mark.user
    async def test_already_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            "/api/v1/expectations/",
            json={
                "dataset_id": DATASETS["postgres_table_products"].key,
                "datasource_id": DATASOURCES["postgres"].key,
                "expectation_type": "expect_column_to_exist",
                "kwargs": {"column": "product_name"},
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        json = response.json()
        json[
            "detail"
        ] == "Table level expectation_type 'ExpectColumnToExist' already exists"

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            "/api/v1/expectations/",
            json={
                "dataset_id": DATASETS["postgres_table_products"].key,
                "datasource_id": DATASOURCES["postgres"].key,
                "expectation_type": "expect_table_row_count_to_be_between",
                "kwargs": {"min_value": 1, "max_value": 100},
            },
        )

        print(response.json())
        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json["expectation_type"] == "expect_table_row_count_to_be_between"
        assert json["create_date"] is not None
        assert json["modified_date"] is not None


@pytest.mark.asyncio
class TestUpdateExpectations:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_expect_column_to_exist'].key}",
            json={},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            "/api/v1/expectations/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0",
            json={
                "dataset_id": DATASETS["postgres_table_products"].key,
                "datasource_id": DATASOURCES["postgres"].key,
                "expectation_type": "expect_column_to_exist",
                "kwargs": {"column": "product_name"},
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_update_datasource(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_expect_column_to_exist'].key}",
            json={
                "dataset_id": DATASETS["postgres_table_products"].key,
                "datasource_id": DATASOURCES["mysql"].key,
                "expectation_type": "expect_column_to_exist",
                "kwargs": {"column": "product_name"},
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        json = response.json()
        json["detail"] == "updates to expectation datasource_id are not supported"

    @pytest.mark.user
    async def test_update_dataset(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_expect_column_to_exist'].key}",
            json={
                "dataset_id": DATASETS["mysql_table_products"].key,
                "datasource_id": DATASOURCES["postgres"].key,
                "expectation_type": "expect_column_to_exist",
                "kwargs": {"column": "product_name"},
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        json = response.json()
        json["detail"] == "updates to expectation dataset_id are not supported"

    @pytest.mark.user
    async def test_allowed(
        self,
        test_client: httpx.AsyncClient,
        expectation_repository: ExpectationRepository,
    ):
        response = await test_client.put(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_expect_column_to_exist'].key}",
            json={
                "dataset_id": DATASETS["postgres_table_products"].key,
                "datasource_id": DATASOURCES["postgres"].key,
                "expectation_type": "expect_column_to_exist",
                "kwargs": {"column": "product_price"},
            },
        )

        assert response.status_code == status.HTTP_200_OK

        updated_expectation = expectation_repository.get(
            EXPECTATIONS["postgres_table_products_expect_column_to_exist"].key
        )

        assert updated_expectation.kwargs.column == "product_price"
        assert (
            updated_expectation.create_date
            == EXPECTATIONS[
                "postgres_table_products_expect_column_to_exist"
            ].create_date
        )
        assert (
            updated_expectation.modified_date
            != EXPECTATIONS[
                "postgres_table_products_expect_column_to_exist"
            ].modified_date
        )

    @pytest.mark.user
    async def test_update_type(
        self,
        test_client: httpx.AsyncClient,
        expectation_repository: ExpectationRepository,
    ):
        response = await test_client.put(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_expect_column_to_exist'].key}",
            json={
                "dataset_id": DATASETS["postgres_table_products"].key,
                "datasource_id": DATASOURCES["postgres"].key,
                "expectation_type": "expect_table_row_count_to_be_between",
                "kwargs": {"min_value": 1, "max_value": 100},
            },
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        new_expectation_key = json["key"]

        with pytest.raises(NotFoundError):
            expectation_repository.get(
                EXPECTATIONS["postgres_table_products_expect_column_to_exist"].key
            )

        new_expectation = expectation_repository.get(new_expectation_key)
        assert (
            new_expectation.expectation_type == "expect_table_row_count_to_be_between"
        )


@pytest.mark.asyncio
class TestDeleteExpectation:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.delete(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_expect_column_to_exist'].key}"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.delete(
            "/api/v1/expectations/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.delete(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_expect_column_to_exist'].key}"
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
class TestEnableExpectation:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_suggested_disabled'].key}/enable"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            "/api/v1/expectations/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0/enable"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_suggested_disabled'].key}/enable"
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json["enabled"] is True


@pytest.mark.asyncio
class TestDisableExpectation:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_expect_column_to_exist'].key}/disable"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            "/api/v1/expectations/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0/disable"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/expectations/{EXPECTATIONS['postgres_table_products_expect_column_to_exist'].key}/disable"
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json["enabled"] is False
