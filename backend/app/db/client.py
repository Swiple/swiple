from opensearchpy import AsyncOpenSearch, OpenSearch
from app.settings import settings
from app.models.users import UserDB


# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts=[{"host": settings.OPENSEARCH_HOST, "port": settings.OPENSEARCH_PORT}],
    http_compress=True,  # enables gzip compression for request bodies
    http_auth=(settings.OPENSEARCH_USERNAME, settings.OPENSEARCH_PASSWORD),
    use_ssl=settings.OPENSEARCH_USE_SSL,
    verify_certs=settings.OPENSEARCH_VERIFY_CERTS,
    ssl_show_warn=settings.OPENSEARCH_SSL_SHOW_WARN,
)


async_client = AsyncOpenSearch(
    hosts=[{"host": settings.OPENSEARCH_HOST, "port": settings.OPENSEARCH_PORT}],
    http_compress=True,  # enables gzip compression for request bodies
    http_auth=(settings.OPENSEARCH_USERNAME, settings.OPENSEARCH_PASSWORD),
    use_ssl=settings.OPENSEARCH_USE_SSL,
    verify_certs=settings.OPENSEARCH_VERIFY_CERTS,
    ssl_show_warn=settings.OPENSEARCH_SSL_SHOW_WARN,
)


async def get_client() -> OpenSearch:
    return client


def get_user_db():
    from fastapi_users_db_opensearch import OpenSearchUserDatabase

    yield OpenSearchUserDatabase(UserDB, async_client)
