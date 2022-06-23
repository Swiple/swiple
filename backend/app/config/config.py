import os

PROJECT_NAME = "DataQuality"
API_VERSION = "/api/v1"
APP = os.getenv("APP")

# Lifetime of HTTP Cookie
# Default: 8 hrs
AUTH_LIFETIME_IN_SECONDS = "28800"

# SECRET_KEY, OAUTH_CLIENT_ID, OAUTH_SECRET, ADMIN_PASSWORD should be stored in a Secret Store
# like AWS Parameter Store or AWS Secrets Manager
# https://swiple.io/docs/configuration/how-to-update-SECRET_KEY
SECRET_KEY = "jSE9Q7_5g1MDpCz7wU1xmcmz27RhSo8nRXCPRjjE6dg="

SWIPLE_API_URL = "http://swiple_api:8000"
SCHEDULER_API_URL = "http://scheduler:8001"
UI_URL = "http://127.0.0.1:3000"

BACKEND_CORS_ORIGINS = [UI_URL, SCHEDULER_API_URL]

SCHEDULER_EXECUTOR_MAX_WORKERS = 10
SCHEDULER_EXECUTOR_KWARGS = None
SCHEDULER_REDIS_DB = 0

# list of Redis connection properties e.g. host, port, password
# https://github.com/redis/redis-py/blob/bedf3c82a55b4b67eed93f686cb17e82f7ab19cd/redis/client.py#L899
SCHEDULER_REDIS_KWARGS = {
    "host": "redis"
}

OPENSEARCH_HOST = "opensearch-node1"
OPENSEARCH_PORT = "9200"
OPENSEARCH_USERNAME = "admin"
OPENSEARCH_PASSWORD = "admin"

USERNAME_AND_PASSWORD_ENABLED = True
# changing ADMIN_EMAIL does not remove the previous user.
ADMIN_EMAIL = "admin@email.com"
ADMIN_PASSWORD = "admin"

GITHUB_OAUTH_ENABLED = False
GITHUB_OAUTH_CLIENT_ID = None
GITHUB_OAUTH_SECRET = None

GOOGLE_OAUTH_ENABLED = False
GOOGLE_OAUTH_CLIENT_ID = None
GOOGLE_OAUTH_SECRET = None

MICROSOFT_OAUTH_ENABLED = False
MICROSOFT_OAUTH_CLIENT_ID = None
MICROSOFT_OAUTH_SECRET = None
MICROSOFT_OAUTH_TENANT = None  # defaults to "common" when not set

OKTA_OAUTH_ENABLED = False
OKTA_OAUTH_CLIENT_ID = None
OKTA_OAUTH_SECRET = None
OKTA_OAUTH_BASE_URL = None
