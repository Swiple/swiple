import asyncio
from typing import AsyncGenerator, Generator

import asgi_lifespan
import httpx
import pytest
import pytest_asyncio
from opensearchpy import OpenSearch
from openmock import _get_openmock

from app.main import app
from app.db.client import get_client
from app.scripts.setup_opensearch import create_indicies


@pytest.fixture(scope="session")
def event_loop():
    """Force the main asyncio loop."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def opensearch_client() -> Generator[OpenSearch, None, None]:
    mock_client = _get_openmock()
    create_indicies(mock_client)
    yield mock_client


@pytest_asyncio.fixture
async def test_client(
    opensearch_client: OpenSearch,
) -> AsyncGenerator[httpx.AsyncClient, None]:
    async with asgi_lifespan.LifespanManager(app):
        app.dependency_overrides[get_client] = lambda: opensearch_client
        async with httpx.AsyncClient(
            app=app, base_url="http://api.swiple.io"
        ) as test_client:
            yield test_client
