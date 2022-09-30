import pytest
from opensearchpy import OpenSearch

from app.repositories.datasource import DatasourceRepository


@pytest.fixture
def repository(opensearch_client: OpenSearch):
    return DatasourceRepository(opensearch_client)


class TestRepositoriesDatasource:
    def test_query_by_name(self, repository: DatasourceRepository):
        result = repository.query_by_name("Test")
        assert result == []
