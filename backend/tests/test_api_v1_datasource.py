import httpx
import pytest
from fastapi import status
from opensearchpy import OpenSearch, RequestError
from pytest_mock import MockerFixture
import requests

from app import constants as c
from app.repositories.datasource import DatasourceRepository
from tests.data import DATASOURCES


@pytest.fixture
def datasource_repository(opensearch_client: OpenSearch):
    return DatasourceRepository(opensearch_client)


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
        assert len(json) == 7


@pytest.mark.asyncio
class TestListDatasources:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/datasources/")

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
            "/api/v1/datasources/", params={"sort_by_key": "invalid_key"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        json = response.json()
        assert json["detail"] == "invalid sort_by_key"

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/datasources/")

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        print(json)
        assert json == [
            {
                "create_date": "2022-10-04 13:37:00.000000+00:00",
                "modified_date": "2022-10-04 13:37:00.000000+00:00",
                "key": "50a58a0b-89e8-4d6f-8b65-6ea328b2cad2",
                "engine": "PostgreSQL",
                "datasource_name": "postgres",
                "description": None,
                "created_by": "admin@email.com",
                "username": "postgres",
                "password": "*****",
                "database": "postgres",
                "host": "postgres",
                "port": 5432,
            },
            {
                "create_date": "2022-10-04 13:37:00.000000+00:00",
                "modified_date": "2022-10-04 13:37:00.000000+00:00",
                "key": "dd19ce80-e020-4a63-9f52-9d0950558df6",
                "engine": "MySQL",
                "datasource_name": "mysql",
                "description": None,
                "created_by": "admin@email.com",
                "username": "mysql",
                "password": "*****",
                "database": "mysql",
                "host": "mysql",
                "port": 3306,
            },
        ]


@pytest.mark.asyncio
class TestGetDatasource:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.get(
            f"/api/v1/datasources/{DATASOURCES['postgres'].key}"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.get(
            "/api/v1/datasources/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.get(
            f"/api/v1/datasources/{DATASOURCES['postgres'].key}"
        )

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json == {
            "create_date": "2022-10-04 13:37:00.000000+00:00",
            "modified_date": "2022-10-04 13:37:00.000000+00:00",
            "key": "50a58a0b-89e8-4d6f-8b65-6ea328b2cad2",
            "engine": "PostgreSQL",
            "datasource_name": "postgres",
            "description": None,
            "created_by": "admin@email.com",
            "username": "postgres",
            "password": "*****",
            "database": "postgres",
            "host": "postgres",
            "port": 5432,
        }


@pytest.mark.asyncio
class TestCreateDatasource:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.post("/api/v1/datasources/", json={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_already_existing_name(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            "/api/v1/datasources",
            json={
                "engine": "PostgreSQL",
                "datasource_name": "postgres",
                "username": "postgres",
                "password": "postgres",
                "database": "postgres",
                "host": "postgres",
                "port": 5432,
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        json = response.json()
        assert json["detail"] == "datasource 'postgres' already exists"

    @pytest.mark.user
    async def test_allowed(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            "/api/v1/datasources",
            json={
                "engine": "PostgreSQL",
                "datasource_name": "postgres_2",
                "username": "postgres",
                "password": "postgres",
                "database": "postgres",
                "host": "postgres",
                "port": 5432,
            },
        )

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json["engine"] == "PostgreSQL"
        assert json["created_by"] == "admin@email.com"
        assert json["create_date"] is not None
        assert json["modified_date"] is not None


@pytest.mark.asyncio
class TestUpdateDatasource:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/datasources/{DATASOURCES['postgres'].key}", json={}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            "/api/v1/datasources/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0",
            json={
                "engine": "PostgreSQL",
                "datasource_name": "mysql",
                "username": "postgres",
                "password": "postgres",
                "database": "postgres",
                "host": "postgres",
                "port": 5432,
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_already_existing_name(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/datasources/{DATASOURCES['postgres'].key}",
            json={
                "engine": "PostgreSQL",
                "datasource_name": "mysql",
                "username": "postgres",
                "password": "postgres",
                "database": "postgres",
                "host": "postgres",
                "port": 5432,
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        json = response.json()
        assert json["detail"] == "Data Source Name 'mysql' already exists"

    @pytest.mark.user
    async def test_password_not_updated(
        self,
        test_client: httpx.AsyncClient,
        datasource_repository: DatasourceRepository,
    ):
        response = await test_client.put(
            f"/api/v1/datasources/{DATASOURCES['postgres'].key}",
            json={
                "engine": "PostgreSQL",
                "datasource_name": "postgres",
                "username": "postgres",
                "password": c.SECRET_MASK,
                "database": "postgres",
                "host": "postgres",
                "port": 5432,
            },
        )

        assert response.status_code == status.HTTP_200_OK

        updated_datasource = datasource_repository.get(DATASOURCES["postgres"].key)

        assert (
            updated_datasource.password.get_decrypted_value()
            == DATASOURCES["postgres"].password.get_decrypted_value()
        )
        assert updated_datasource.create_date == DATASOURCES["postgres"].create_date
        assert updated_datasource.modified_date != DATASOURCES["postgres"].modified_date

    @pytest.mark.user
    async def test_updated_password(
        self,
        test_client: httpx.AsyncClient,
        datasource_repository: DatasourceRepository,
    ):
        response = await test_client.put(
            f"/api/v1/datasources/{DATASOURCES['postgres'].key}",
            json={
                "engine": "PostgreSQL",
                "datasource_name": "postgres",
                "username": "postgres",
                "password": "updated_password",
                "database": "postgres",
                "host": "postgres",
                "port": 5432,
            },
        )

        assert response.status_code == status.HTTP_200_OK

        updated_datasource = datasource_repository.get(DATASOURCES["postgres"].key)

        assert updated_datasource.password.get_decrypted_value() == "updated_password"
        assert updated_datasource.create_date == DATASOURCES["postgres"].create_date
        assert updated_datasource.modified_date != DATASOURCES["postgres"].modified_date


@pytest.mark.asyncio
class TestDeleteDatasource:
    async def test_unauthorized(self, test_client: httpx.AsyncClient):
        response = await test_client.delete(
            f"/api/v1/datasources/{DATASOURCES['postgres'].key}"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.user
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.delete(
            "/api/v1/datasources/5ecf8e33-2c19-4ed7-a11a-def2cd494ef0"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.user
    async def test_allowed(self, mocker: MockerFixture, test_client: httpx.AsyncClient):
        # Mock requests.delete request
        # This shall be removed when we delete the schedules without an HTTP request to our own API
        mocker.patch.object(requests, "delete", return_value=None)

        response = await test_client.delete(
            f"/api/v1/datasources/{DATASOURCES['postgres'].key}"
        )

        assert response.status_code == status.HTTP_200_OK
