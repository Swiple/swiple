import asyncio
from typing import AsyncGenerator

import asgi_lifespan
import httpx
import pytest
import pytest_asyncio

from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Force the main asyncio loop."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with asgi_lifespan.LifespanManager(app):
        async with httpx.AsyncClient(
            app=app, base_url="http://api.swiple.io"
        ) as test_client:
            yield test_client
