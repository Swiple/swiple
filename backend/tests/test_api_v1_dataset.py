import datetime
from unittest.mock import MagicMock
import httpx
import pytest
from fastapi import status
from opensearchpy import OpenSearch, RequestError
from pydantic.errors import Decimal
from pytest_mock import MockerFixture
import requests

from app.core.runner import Runner
from app.core.sample import GetSampleException
from app.models.dataset import Sample
from app.repositories.dataset import DatasetRepository
from tests.data import DATASETS, DATASOURCES
from great_expectations.validator.validator import Validator


@pytest.fixture
def dataset_repository(opensearch_client: OpenSearch):
    return DatasetRepository(opensearch_client)


@pytest.fixture
def mock_sa_connection(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("sqlalchemy.engine.Engine.connect", MagicMock())


@pytest.fixture
def mock_action_dispatcher(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("app.core.actions.action_dispatcher.dispatch")


@pytest.fixture
def get_dataset_sample_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("app.api.api_v1.endpoints.dataset.get_dataset_sample")


@pytest.fixture
def sample_columns_and_rows(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("app.core.sample.get_columns_and_rows")
    mock.return_value = _get_columns_and_rows_return_values()
    return mock


@pytest.fixture
def empty_table_sample_columns_and_rows(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("app.core.sample.get_columns_and_rows")
    mock.return_value = ([], [])
    return mock


@pytest.fixture
def runner_mock(mocker: MockerFixture) -> MagicMock:
    class_mock = mocker.patch("app.core.runner.Runner", spec=Runner)
    instance_mock = class_mock.return_value
    return instance_mock


@pytest.fixture
def validator_mock(mocker: MockerFixture) -> MagicMock:
    class_mock = mocker.patch("great_expectations.validator.validator.Validator", spec=Validator)
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
        assert json == [{
            'connector_type': 'RuntimeDataConnector',
            'create_date': '2022-10-04 13:37:00.000000+00:00',
            'created_by': 'admin@email.com',
            'database': '',
            'dataset_name': 'main.LINEITEM',
            'datasource_id': '9034f199-bd74-415f-990e-9d6cc8c56589',
            'datasource_name': 'sqlite',
            'description': None,
            'engine': 'SQLite',
            'key': 'ce530620-e977-4290-b07e-4c3d5b3cae9c',
            'modified_date': '2022-10-04 13:37:00.000000+00:00',
            'runtime_parameters': None,
            'sample': None,
            'sampling': None},
            {'connector_type': 'RuntimeDataConnector',
             'create_date': '2022-10-04 13:37:00.000000+00:00',
             'created_by': 'admin@email.com',
             'database': '',
             'dataset_name': 'sqlite_view_part',
             'datasource_id': '9034f199-bd74-415f-990e-9d6cc8c56589',
             'datasource_name': 'sqlite',
             'description': None,
             'engine': 'SQLite',
             'key': '49f5fe7c-d8d5-4766-91e9-49a27010b638',
             'modified_date': '2022-10-04 13:37:00.000000+00:00',
             'runtime_parameters': {'query': ' select * from main.PART',
                                    'schema': 'main'},
             'sample': None,
             'sampling': None},
            {'connector_type': 'RuntimeDataConnector',
             'create_date': '2022-10-04 13:37:00.000000+00:00',
             'created_by': 'admin@email.com',
             'database': 'postgres',
             'dataset_name': 'schema.postgres_table_products',
             'datasource_id': '50a58a0b-89e8-4d6f-8b65-6ea328b2cad2',
             'datasource_name': 'postgres',
             'description': None,
             'engine': 'PostgreSQL',
             'key': '5b65eae9-600e-4933-9bad-78477e0ab98e',
             'modified_date': '2022-10-04 13:37:00.000000+00:00',
             'runtime_parameters': None,
             'sample': None,
             'sampling': None},
            {'connector_type': 'RuntimeDataConnector',
             'create_date': '2022-10-04 13:37:00.000000+00:00',
             'created_by': 'admin@email.com',
             'database': 'postgres',
             'dataset_name': 'postgres_view_orders',
             'datasource_id': '50a58a0b-89e8-4d6f-8b65-6ea328b2cad2',
             'datasource_name': 'postgres',
             'description': None,
             'engine': 'PostgreSQL',
             'key': '4b252091-6d0d-4beb-9552-3764cfe8cbae',
             'modified_date': '2022-10-04 13:37:00.000000+00:00',
             'runtime_parameters': {'query': ' select * from schema.orders limit 100 ; ',
                                    'schema': 'schema'},
             'sample': None,
             'sampling': None},
            {'connector_type': 'RuntimeDataConnector',
             'create_date': '2022-10-04 13:37:00.000000+00:00',
             'created_by': 'admin@email.com',
             'database': 'mysql',
             'dataset_name': 'schema.mysql_table_products',
             'datasource_id': 'dd19ce80-e020-4a63-9f52-9d0950558df6',
             'datasource_name': 'mysql',
             'description': None,
             'engine': 'MySQL',
             'key': '5b6adc59-d92d-4b75-9d7e-7e1e6f4392a7',
             'modified_date': '2022-10-04 13:37:00.000000+00:00',
             'runtime_parameters': None,
             'sample': None,
             'sampling': None}]

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
            "dataset_name": "schema.postgres_table_products",
            "description": None,
            "runtime_parameters": None,
            "engine": "PostgreSQL",
            "sample": None,
            "sampling": None,
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
                "dataset_name": "schema.postgres_table_products",
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        json = response.json()
        assert (
            json["detail"]
            == "dataset 'postgres.schema.postgres_table_products' already exists"
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
        assert json["detail"] == "get_sample_error"

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
                "dataset_name": "schema.postgres_table_products",
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
                "dataset_name": "schema.postgres_table_products",
                "runtime_parameters": {"schema": "products"},
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        json = response.json()
        assert json["detail"] == "updates to dataset datasource_id are not supported"

    @pytest.mark.user
    async def test_conflicting_name(self, test_client: httpx.AsyncClient):
        response = await test_client.put(
            f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}",
            json={
                "datasource_id": DATASOURCES["postgres"].key,
                "datasource_name": DATASOURCES["postgres"].datasource_name,
                "database": DATASOURCES["postgres"].database,
                "dataset_name": DATASETS["postgres_view_orders"].dataset_name,
                "runtime_parameters": {"schema": "orders"},
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        json = response.json()
        assert (
            json["detail"]
            == "dataset 'postgres.orders.postgres_view_orders' already exists"
        )

    @pytest.mark.user
    async def test_allowed(
        self, test_client: httpx.AsyncClient, dataset_repository: DatasetRepository,
    ):
        response = await test_client.put(
            f"/api/v1/datasets/{DATASETS['sqlite_table_lineitem'].key}",
            json={
                "datasource_id": DATASOURCES["sqlite"].key,
                "datasource_name": DATASOURCES["sqlite"].datasource_name,
                "database": DATASOURCES["sqlite"].database,
                "dataset_name": "main.ORDERS",
            },
        )

        assert response.status_code == status.HTTP_200_OK

        updated_dataset = dataset_repository.get(
            DATASETS["sqlite_table_lineitem"].key
        )

        assert updated_dataset.dataset_name == "main.ORDERS"
        assert (
            updated_dataset.create_date == DATASETS["sqlite_table_lineitem"].create_date
        )
        assert (
            updated_dataset.modified_date != DATASETS["sqlite_table_lineitem"].modified_date
        )
        assert updated_dataset.sample != DATASETS["sqlite_table_lineitem"].sample


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
                "dataset_name": "schema.postgres_table_users",
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        json = response.json()
        assert json["detail"] == "get_sample_error"

    @pytest.mark.user
    async def test_allowed(
        self, test_client: httpx.AsyncClient
    ):
        response = await test_client.post(
            "/api/v1/datasets/sample",
            json={
                "datasource_id": DATASOURCES["sqlite"].key,
                "datasource_name": DATASOURCES["sqlite"].datasource_name,
                "database": DATASOURCES["sqlite"].database,
                "dataset_name": "main.NATION",
            },
        )

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json == {
            'columns': ['N_NATIONKEY', 'N_NAME', 'N_REGIONKEY', 'N_COMMENT'],
            'rows': [
                {'N_COMMENT': ' haggle. carefully final deposits detect slyly agai', 'N_NAME': 'ALGERIA',
                 'N_NATIONKEY': 0, 'N_REGIONKEY': 0},
                {'N_COMMENT': 'al foxes promise slyly according to the regular accounts. bold requests alon',
                 'N_NAME': 'ARGENTINA', 'N_NATIONKEY': 1, 'N_REGIONKEY': 1},
                {'N_COMMENT': 'y alongside of the pending deposits. carefully special packages are about the ironic ' \
                              'forges. slyly special ', 'N_NAME': 'BRAZIL', 'N_NATIONKEY': 2, 'N_REGIONKEY': 1},
                {'N_COMMENT': 'eas hang ironic, silent packages. slyly regular packages are furiously over the ' \
                              'tithes. fluffily bold', 'N_NAME': 'CANADA', 'N_NATIONKEY': 3, 'N_REGIONKEY': 1},
                {'N_COMMENT': 'y above the carefully unusual theodolites. final dugouts are quickly across the ' \
                              'furiously regular d', 'N_NAME': 'EGYPT', 'N_NATIONKEY': 4, 'N_REGIONKEY': 4},
                {'N_COMMENT': 'ven packages wake quickly. regu', 'N_NAME': 'ETHIOPIA', 'N_NATIONKEY': 5,
                 'N_REGIONKEY': 0},
                {'N_COMMENT': 'refully final requests. regular, ironi', 'N_NAME': 'FRANCE', 'N_NATIONKEY': 6,
                 'N_REGIONKEY': 3},
                {'N_COMMENT': 'l platelets. regular accounts x-ray: unusual, regular acco', 'N_NAME': 'GERMANY',
                 'N_NATIONKEY': 7, 'N_REGIONKEY': 3},
                {'N_COMMENT': 'ss excuses cajole slyly across the packages. deposits print aroun', 'N_NAME': 'INDIA',
                 'N_NATIONKEY': 8, 'N_REGIONKEY': 2},
                {'N_COMMENT': ' slyly express asymptotes. regular deposits haggle slyly. carefully ironic hockey ' \
                              'players sleep blithely. carefull', 'N_NAME': 'INDONESIA', 'N_NATIONKEY': 9,
                 'N_REGIONKEY': 2}
            ]
        }


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
        assert json["detail"] == "get_sample_error"

    # TODO uncomment once this GH ISSUE is resolved.
    # https://github.com/great-expectations/great_expectations/issues/6463#issuecomment-1334476484
    # @pytest.mark.user
    # async def test_get_table_sample_exception(
    #     self, test_client: httpx.AsyncClient, mock_sa_connection, empty_table_sample_columns_and_rows
    # ):
    #     response = await test_client.put(
    #         f"/api/v1/datasets/{DATASETS['postgres_table_products'].key}/sample",
    #         json={},
    #     )
    #
    #     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    #
    #     json = response.json()
    #     assert json["detail"] == "No columns included in statement."

    @pytest.mark.user
    async def test_physical_table_sample(
        self,
        test_client: httpx.AsyncClient,
        dataset_repository: DatasetRepository,
        sample_columns_and_rows
    ):
        response = await test_client.put(
            f"/api/v1/datasets/{DATASETS['sqlite_table_lineitem'].key}/sample",
            json={},
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json["key"] == DATASETS["sqlite_table_lineitem"].key

        updated_dataset = dataset_repository.get(
            DATASETS["sqlite_table_lineitem"].key
        )

        assert updated_dataset.sample == Sample(
            columns=['L_ORDERKEY', 'L_PARTKEY', 'L_SUPPKEY', 'L_LINENUMBER', 'L_QUANTITY', 'L_EXTENDEDPRICE', 'L_DISCOUNT', 'L_TAX', 'L_RETURNFLAG', 'L_LINESTATUS', 'L_SHIPDATE', 'L_COMMITDATE', 'L_RECEIPTDATE', 'L_SHIPINSTRUCT', 'L_SHIPMODE', 'L_COMMENT'],
            rows=[
                {'L_ORDERKEY': 1, 'L_PARTKEY': 1552, 'L_SUPPKEY': 93, 'L_LINENUMBER': 1, 'L_QUANTITY': 17, 'L_EXTENDEDPRICE': 24710.35, 'L_DISCOUNT': 0.04, 'L_TAX': 0.02, 'L_RETURNFLAG': 'N', 'L_LINESTATUS': 'O', 'L_SHIPDATE': '1996-03-13', 'L_COMMITDATE': '1996-02-12', 'L_RECEIPTDATE': '1996-03-22', 'L_SHIPINSTRUCT': 'DELIVER IN PERSON', 'L_SHIPMODE': 'TRUCK', 'L_COMMENT': 'egular courts above the'},
                {'L_ORDERKEY': 1, 'L_PARTKEY': 674, 'L_SUPPKEY': 75, 'L_LINENUMBER': 2, 'L_QUANTITY': 36, 'L_EXTENDEDPRICE': 56688.12, 'L_DISCOUNT': 0.09, 'L_TAX': 0.06, 'L_RETURNFLAG': 'N', 'L_LINESTATUS': 'O', 'L_SHIPDATE': '1996-04-12', 'L_COMMITDATE': '1996-02-28', 'L_RECEIPTDATE': '1996-04-20', 'L_SHIPINSTRUCT': 'TAKE BACK RETURN', 'L_SHIPMODE': 'MAIL', 'L_COMMENT': 'ly final dependencies: slyly bold '},
                {'L_ORDERKEY': 1, 'L_PARTKEY': 637, 'L_SUPPKEY': 38, 'L_LINENUMBER': 3, 'L_QUANTITY': 8, 'L_EXTENDEDPRICE': 12301.04, 'L_DISCOUNT': 0.1, 'L_TAX': 0.02, 'L_RETURNFLAG': 'N', 'L_LINESTATUS': 'O', 'L_SHIPDATE': '1996-01-29', 'L_COMMITDATE': '1996-03-05', 'L_RECEIPTDATE': '1996-01-31', 'L_SHIPINSTRUCT': 'TAKE BACK RETURN', 'L_SHIPMODE': 'REG AIR', 'L_COMMENT': 'riously. regular, express dep'},
                {'L_ORDERKEY': 1, 'L_PARTKEY': 22, 'L_SUPPKEY': 48, 'L_LINENUMBER': 4, 'L_QUANTITY': 28, 'L_EXTENDEDPRICE': 25816.56, 'L_DISCOUNT': 0.09, 'L_TAX': 0.06, 'L_RETURNFLAG': 'N', 'L_LINESTATUS': 'O', 'L_SHIPDATE': '1996-04-21', 'L_COMMITDATE': '1996-03-30', 'L_RECEIPTDATE': '1996-05-16', 'L_SHIPINSTRUCT': 'NONE', 'L_SHIPMODE': 'AIR', 'L_COMMENT': 'lites. fluffily even de'},
                {'L_ORDERKEY': 1, 'L_PARTKEY': 241, 'L_SUPPKEY': 23, 'L_LINENUMBER': 5, 'L_QUANTITY': 24, 'L_EXTENDEDPRICE': 27389.76, 'L_DISCOUNT': 0.1, 'L_TAX': 0.04, 'L_RETURNFLAG': 'N', 'L_LINESTATUS': 'O', 'L_SHIPDATE': '1996-03-30', 'L_COMMITDATE': '1996-03-14', 'L_RECEIPTDATE': '1996-04-01', 'L_SHIPINSTRUCT': 'NONE', 'L_SHIPMODE': 'FOB', 'L_COMMENT': ' pending foxes. slyly re'},
                {'L_ORDERKEY': 1, 'L_PARTKEY': 157, 'L_SUPPKEY': 10, 'L_LINENUMBER': 6, 'L_QUANTITY': 32, 'L_EXTENDEDPRICE': 33828.8, 'L_DISCOUNT': 0.07, 'L_TAX': 0.02, 'L_RETURNFLAG': 'N', 'L_LINESTATUS': 'O', 'L_SHIPDATE': '1996-01-30', 'L_COMMITDATE': '1996-02-07', 'L_RECEIPTDATE': '1996-02-03', 'L_SHIPINSTRUCT': 'DELIVER IN PERSON', 'L_SHIPMODE': 'MAIL', 'L_COMMENT': 'arefully slyly ex'},
                {'L_ORDERKEY': 2, 'L_PARTKEY': 1062, 'L_SUPPKEY': 33, 'L_LINENUMBER': 1, 'L_QUANTITY': 38, 'L_EXTENDEDPRICE': 36596.28, 'L_DISCOUNT': 0.0, 'L_TAX': 0.05, 'L_RETURNFLAG': 'N', 'L_LINESTATUS': 'O', 'L_SHIPDATE': '1997-01-28', 'L_COMMITDATE': '1997-01-14', 'L_RECEIPTDATE': '1997-02-02', 'L_SHIPINSTRUCT': 'TAKE BACK RETURN', 'L_SHIPMODE': 'RAIL', 'L_COMMENT': 'ven requests. deposits breach a'},
                {'L_ORDERKEY': 3, 'L_PARTKEY': 43, 'L_SUPPKEY': 19, 'L_LINENUMBER': 1, 'L_QUANTITY': 45, 'L_EXTENDEDPRICE': 42436.8, 'L_DISCOUNT': 0.06, 'L_TAX': 0.0, 'L_RETURNFLAG': 'R', 'L_LINESTATUS': 'F', 'L_SHIPDATE': '1994-02-02', 'L_COMMITDATE': '1994-01-04', 'L_RECEIPTDATE': '1994-02-23', 'L_SHIPINSTRUCT': 'NONE', 'L_SHIPMODE': 'AIR', 'L_COMMENT': 'ongside of the furiously brave acco'},
                {'L_ORDERKEY': 3, 'L_PARTKEY': 191, 'L_SUPPKEY': 70, 'L_LINENUMBER': 2, 'L_QUANTITY': 49, 'L_EXTENDEDPRICE': 53468.31, 'L_DISCOUNT': 0.1, 'L_TAX': 0.0, 'L_RETURNFLAG': 'R', 'L_LINESTATUS': 'F', 'L_SHIPDATE': '1993-11-09', 'L_COMMITDATE': '1993-12-20', 'L_RECEIPTDATE': '1993-11-24', 'L_SHIPINSTRUCT': 'TAKE BACK RETURN', 'L_SHIPMODE': 'RAIL', 'L_COMMENT': ' unusual accounts. eve'},
                {'L_ORDERKEY': 3, 'L_PARTKEY': 1285, 'L_SUPPKEY': 60, 'L_LINENUMBER': 3, 'L_QUANTITY': 27, 'L_EXTENDEDPRICE': 32029.56, 'L_DISCOUNT': 0.06, 'L_TAX': 0.07, 'L_RETURNFLAG': 'A', 'L_LINESTATUS': 'F', 'L_SHIPDATE': '1994-01-16', 'L_COMMITDATE': '1993-11-22', 'L_RECEIPTDATE': '1994-01-23', 'L_SHIPINSTRUCT': 'DELIVER IN PERSON', 'L_SHIPMODE': 'SHIP', 'L_COMMENT': 'nal foxes wake. '},
            ])
        assert (
            updated_dataset.create_date
            == DATASETS["sqlite_table_lineitem"].create_date
        )
        assert (
            updated_dataset.modified_date
            != DATASETS["sqlite_table_lineitem"].modified_date
        )

    @pytest.mark.user
    async def test_query_sample(
        self,
        test_client: httpx.AsyncClient,
        dataset_repository: DatasetRepository,
    ):
        response = await test_client.put(
            f"/api/v1/datasets/{DATASETS['sqlite_view_part'].key}/sample",
            json={},
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json["key"] == DATASETS["sqlite_view_part"].key

        updated_dataset = dataset_repository.get(
            DATASETS["sqlite_view_part"].key
        )
        assert updated_dataset.sample == Sample(
            columns=['P_PARTKEY', 'P_NAME', 'P_MFGR', 'P_BRAND', 'P_TYPE', 'P_SIZE', 'P_CONTAINER', 'P_RETAILPRICE', 'P_COMMENT'],
            rows=[
                {'key': 0, 'P_PARTKEY': 1, 'P_NAME': 'goldenrod lavender spring chocolate lace', 'P_MFGR': 'Manufacturer#1', 'P_BRAND': 'Brand#13', 'P_TYPE': 'PROMO BURNISHED COPPER', 'P_SIZE': 7, 'P_CONTAINER': 'JUMBO PKG', 'P_RETAILPRICE': 901, 'P_COMMENT': 'ly. slyly ironi'},
                {'key': 1, 'P_PARTKEY': 2, 'P_NAME': 'blush thistle blue yellow saddle', 'P_MFGR': 'Manufacturer#1', 'P_BRAND': 'Brand#13', 'P_TYPE': 'LARGE BRUSHED BRASS', 'P_SIZE': 1, 'P_CONTAINER': 'LG CASE', 'P_RETAILPRICE': 902, 'P_COMMENT': 'lar accounts amo'},
                {'key': 2, 'P_PARTKEY': 3, 'P_NAME': 'spring green yellow purple cornsilk', 'P_MFGR': 'Manufacturer#4', 'P_BRAND': 'Brand#42', 'P_TYPE': 'STANDARD POLISHED BRASS', 'P_SIZE': 21, 'P_CONTAINER': 'WRAP CASE', 'P_RETAILPRICE': 903, 'P_COMMENT': 'egular deposits hag'},
                {'key': 3, 'P_PARTKEY': 4, 'P_NAME': 'cornflower chocolate smoke green pink', 'P_MFGR': 'Manufacturer#3', 'P_BRAND': 'Brand#34', 'P_TYPE': 'SMALL PLATED BRASS', 'P_SIZE': 14, 'P_CONTAINER': 'MED DRUM', 'P_RETAILPRICE': 904, 'P_COMMENT': 'p furiously r'},
                {'key': 4, 'P_PARTKEY': 5, 'P_NAME': 'forest brown coral puff cream', 'P_MFGR': 'Manufacturer#3', 'P_BRAND': 'Brand#32', 'P_TYPE': 'STANDARD POLISHED TIN', 'P_SIZE': 15, 'P_CONTAINER': 'SM PKG', 'P_RETAILPRICE': 905, 'P_COMMENT': ' wake carefully '},
                {'key': 5, 'P_PARTKEY': 6, 'P_NAME': 'bisque cornflower lawn forest magenta', 'P_MFGR': 'Manufacturer#2', 'P_BRAND': 'Brand#24', 'P_TYPE': 'PROMO PLATED STEEL', 'P_SIZE': 4, 'P_CONTAINER': 'MED BAG', 'P_RETAILPRICE': 906, 'P_COMMENT': 'sual a'},
                {'key': 6, 'P_PARTKEY': 7, 'P_NAME': 'moccasin green thistle khaki floral', 'P_MFGR': 'Manufacturer#1', 'P_BRAND': 'Brand#11', 'P_TYPE': 'SMALL PLATED COPPER', 'P_SIZE': 45, 'P_CONTAINER': 'SM BAG', 'P_RETAILPRICE': 907, 'P_COMMENT': 'lyly. ex'},
                {'key': 7, 'P_PARTKEY': 8, 'P_NAME': 'misty lace thistle snow royal', 'P_MFGR': 'Manufacturer#4', 'P_BRAND': 'Brand#44', 'P_TYPE': 'PROMO BURNISHED TIN', 'P_SIZE': 41, 'P_CONTAINER': 'LG DRUM', 'P_RETAILPRICE': 908, 'P_COMMENT': 'eposi'},
                {'key': 8, 'P_PARTKEY': 9, 'P_NAME': 'thistle dim navajo dark gainsboro', 'P_MFGR': 'Manufacturer#4', 'P_BRAND': 'Brand#43', 'P_TYPE': 'SMALL BURNISHED STEEL', 'P_SIZE': 12, 'P_CONTAINER': 'WRAP CASE', 'P_RETAILPRICE': 909, 'P_COMMENT': 'ironic foxe'},
                {'key': 9, 'P_PARTKEY': 10, 'P_NAME': 'linen pink saddle puff powder', 'P_MFGR': 'Manufacturer#5', 'P_BRAND': 'Brand#54', 'P_TYPE': 'LARGE BURNISHED STEEL', 'P_SIZE': 44, 'P_CONTAINER': 'LG CAN', 'P_RETAILPRICE': 910.01, 'P_COMMENT': 'ithely final deposit'},
            ]
        )
        assert (
            updated_dataset.create_date
            == DATASETS["postgres_view_orders"].create_date
        )
        assert (
            updated_dataset.modified_date
            != DATASETS["postgres_view_orders"].modified_date
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
        self, test_client: httpx.AsyncClient,
        mock_action_dispatcher: MagicMock,
    ):
        response = await test_client.post(
            f"/api/v1/datasets/{DATASETS['sqlite_table_lineitem'].key}/suggest",
            json={},
        )

        suggestions: list = response.json()

        # enable suggested validations
        for suggestion in suggestions:
            await test_client.put(
                f"/api/v1/expectations/{suggestion['key']}/enable"
            )

        # validate enabled suggestions/expectations
        response = await test_client.post(
            f"/api/v1/datasets/{DATASETS['sqlite_table_lineitem'].key}/validate",
            json={},
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json["results"]) == len(suggestions)


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
    async def test_physical_table(
        self, test_client: httpx.AsyncClient
    ):
        response = await test_client.post(
            f"/api/v1/datasets/{DATASETS['sqlite_table_lineitem'].key}/suggest",
            json={},
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json) > 0

    @pytest.mark.user
    async def test_query_table(
        self, test_client: httpx.AsyncClient
    ):
        response = await test_client.post(
            f"/api/v1/datasets/{DATASETS['sqlite_view_part'].key}/suggest",
            json={},
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json) > 0


def _get_columns_and_rows_return_values():
    return (
        ['o_orderkey', 'o_custkey', 'o_orderstatus', 'o_totalprice', 'o_orderdate', 'o_orderpriority', 'o_clerk',
         'o_shippriority', 'o_comment'],
        [
            (
                Decimal('4200001'),
                Decimal('13726'), 'F',
                Decimal('99406.41'),
                datetime.date(1994, 2, 21),
                '3-MEDIUM',
                'Clerk#000000128',
                Decimal('0'),
                'eep. final deposits are after t',
            ),
            (
                Decimal('4200002'),
                Decimal('129376'),
                'O',
                Decimal('256838.41'),
                datetime.date(1997, 4, 14),
                '4-NOT SPECIFIED', 'Clerk#000000281',
                Decimal('0'),
            )
        ]
    )