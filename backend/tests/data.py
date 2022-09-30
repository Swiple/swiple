from typing import Type
from opensearchpy import OpenSearch

from app.models.datasource import Datasource, PostgreSQL, Engine
from app.repositories.base import M, R
from app.repositories.datasource import DatasourceRepository

DATASOURCES: dict[str, Datasource] = {
    "postgres": PostgreSQL(
        datasource_name="postgres",
        engine=Engine.POSTGRESQL,
        username="postgres",
        password="postgres",
        database="postgres",
        host="postgres",
        port=5432,
    ),
}

TEST_DATA: dict[Type[R], dict[str, M]] = {
    DatasourceRepository: DATASOURCES,
}


def create_test_data(client: OpenSearch):
    for repository_class in TEST_DATA:
        repository = repository_class(client)
        for object in TEST_DATA[repository_class].values():
            repository.create(object.key, object)
