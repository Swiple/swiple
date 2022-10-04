from typing import Type
from opensearchpy import OpenSearch

from app.models.datasource import Datasource, MySQL, PostgreSQL, Engine
from app.repositories.base import M, R
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

TEST_DATA: dict[Type[R], dict[str, M]] = {
    DatasourceRepository: DATASOURCES,
}


def create_test_data(client: OpenSearch):
    for repository_class in TEST_DATA:
        repository = repository_class(client)
        for object in TEST_DATA[repository_class].values():
            repository.create(object.key, object)
