import asyncio
from typing import AsyncGenerator, Generator, Optional

import asgi_lifespan
import httpx
import pytest
import pytest_asyncio
from opensearchpy import OpenSearch

from app.core.users import current_active_user
from app.db.client import get_client
from app.main import app
from app.models.auth import User
from app.scripts.setup_opensearch import create_indicies
from tests.data import create_test_data
from tests.fake_opensearch import FakeOpenSearch


@pytest.fixture(scope="session")
def event_loop():
    """Force the main asyncio loop."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def opensearch_client() -> Generator[OpenSearch, None, None]:
    mock_client = FakeOpenSearch()
    create_indicies(mock_client)
    create_test_data(mock_client)
    yield mock_client


@pytest.fixture
def user(request: pytest.FixtureRequest) -> Optional[User]:
    marker = request.node.get_closest_marker("user")
    if marker is None:
        return None

    user = User(email="admin@email.com")
    return user


@pytest_asyncio.fixture
async def test_client(
    opensearch_client: OpenSearch,
    user: Optional[User],
) -> AsyncGenerator[httpx.AsyncClient, None]:
    async with asgi_lifespan.LifespanManager(app):
        app.dependency_overrides[get_client] = lambda: opensearch_client
        if user is not None:
            app.dependency_overrides[current_active_user] = lambda: user
        async with httpx.AsyncClient(
            app=app, base_url="http://api.swiple.io"
        ) as test_client:
            yield test_client
    app.dependency_overrides = {}
