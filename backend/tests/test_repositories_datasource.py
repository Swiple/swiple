import pytest
from opensearchpy import OpenSearch

from app.repositories.datasource import DatasourceRepository
from tests.data import DATASOURCES


@pytest.fixture
def repository(opensearch_client: OpenSearch):
    return DatasourceRepository(opensearch_client)


class TestRepositoriesDatasource:
    def test_count(self, repository: DatasourceRepository):
        count = repository.count({"query": {}})
        assert count == len(DATASOURCES)
