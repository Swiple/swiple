from typing import Type
from opensearchpy import OpenSearch

from app.models.datasource import Datasource, MySQL, PostgreSQL, Engine
from app.models.dataset import Dataset
from app.models.validation import Validation
from app.repositories.base import M, R
from app.repositories.dataset import DatasetRepository
from app.repositories.datasource import DatasourceRepository

DATASOURCES: dict[str, Datasource] = {
    "postgres": PostgreSQL(
        key="50a58a0b-89e8-4d6f-8b65-6ea328b2cad2",
        create_date="2022-10-04 13:37:00.000000+00:00",
        modified_date="2022-10-04 13:37:00.000000+00:00",
        datasource_name="postgres",
        created_by="admin@email.com",
        engine=Engine.POSTGRESQL,
        username="postgres",
        password="postgres",
        database="postgres",
        host="postgres",
        port=5432,
    ),
    "mysql": MySQL(
        key="dd19ce80-e020-4a63-9f52-9d0950558df6",
        create_date="2022-10-04 13:37:00.000000+00:00",
        modified_date="2022-10-04 13:37:00.000000+00:00",
        datasource_name="mysql",
        created_by="admin@email.com",
        engine=Engine.MYSQL,
        username="mysql",
        password="mysql",
        database="mysql",
        host="mysql",
        port=3306,
    ),
}

DATASETS: dict[str, Dataset] = {
    "postgres_table_products": Dataset(
        key="5b65eae9-600e-4933-9bad-78477e0ab98e",
        create_date="2022-10-04 13:37:00.000000+00:00",
        modified_date="2022-10-04 13:37:00.000000+00:00",
        created_by="admin@email.com",
        engine=Engine.POSTGRESQL,
        datasource_id=DATASOURCES["postgres"].key,
        datasource_name=DATASOURCES["postgres"].datasource_name,
        database=DATASOURCES["postgres"].database,
        dataset_name="postgres_table_products",
        runtime_parameters={"schema": "products"},
    ),
    "postgres_table_orders": Dataset(
        key="4b252091-6d0d-4beb-9552-3764cfe8cbae",
        create_date="2022-10-04 13:37:00.000000+00:00",
        modified_date="2022-10-04 13:37:00.000000+00:00",
        created_by="admin@email.com",
        engine=Engine.POSTGRESQL,
        datasource_id=DATASOURCES["postgres"].key,
        datasource_name=DATASOURCES["postgres"].datasource_name,
        database=DATASOURCES["postgres"].database,
        dataset_name="postgres_table_orders",
        runtime_parameters={"schema": "orders"},
    ),
    "mysql_table_products": Dataset(
        key="5b6adc59-d92d-4b75-9d7e-7e1e6f4392a7",
        create_date="2022-10-04 13:37:00.000000+00:00",
        modified_date="2022-10-04 13:37:00.000000+00:00",
        created_by="admin@email.com",
        engine=Engine.MYSQL,
        datasource_id=DATASOURCES["mysql"].key,
        datasource_name=DATASOURCES["mysql"].datasource_name,
        database=DATASOURCES["mysql"].database,
        dataset_name="mysql_table_products",
        runtime_parameters={"schema": "products"},
    ),
}

TEST_DATA: dict[Type[R], dict[str, M]] = {
    DatasourceRepository: DATASOURCES,
    DatasetRepository: DATASETS,
}


def create_test_data(client: OpenSearch):
    for repository_class in TEST_DATA:
        repository = repository_class(client)
        for object in TEST_DATA[repository_class].values():
            repository.create(object.key, object)


def create_validation_object(datasource_id: str, dataset_id: str) -> Validation:
    return Validation(
        meta={
            "great_expectations_version": "1.0.0",
            "expectation_suite_name": "expectation_suite_name",
            "run_id": {"run_time": "run_time", "run_name": "run_name"},
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
            "datasource_id": datasource_id,
            "dataset_id": dataset_id,
        },
        statistics={
            "evaluated_expectations": 100,
            "successful_expectations": 90,
            "unsuccessful_expectations": 10,
            "success_percent": 0.1,
        },
        results=[],
        success=False,
        evaluation_parameters={},
    )
