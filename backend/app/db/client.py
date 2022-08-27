from app.settings import settings
from app.models.auth import UserDB
from opensearchpy import AsyncOpenSearch, OpenSearch


# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts=[{'host': settings.OPENSEARCH_HOST, 'port': settings.OPENSEARCH_PORT}],
    http_compress=True,  # enables gzip compression for request bodies
    http_auth=(settings.OPENSEARCH_USERNAME, settings.OPENSEARCH_PASSWORD),
    # client_cert = client_cert_path,
    # client_key = client_key_path,
    use_ssl=settings.IS_SSL,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    # ca_certs=ca_certs_path
)


async_client = AsyncOpenSearch(
    hosts=[{'host': settings.OPENSEARCH_HOST, 'port': settings.OPENSEARCH_PORT}],
    http_auth=(settings.OPENSEARCH_USERNAME, settings.OPENSEARCH_PASSWORD),
    use_ssl=settings.IS_SSL,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,

)


def get_user_db():
    from fastapi_users_db_opensearch import OpenSearchUserDatabase
    yield OpenSearchUserDatabase(UserDB, async_client)


