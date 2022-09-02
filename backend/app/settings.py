from typing import List, Union, Literal
from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    EmailStr,
    Field,
    validator,
    root_validator,
)


class Settings(BaseSettings):
    PRODUCTION: bool

    # https://swiple.io/docs/configuration/how-to-update-SECRET_KEY
    SECRET_KEY: str

    # Changing ADMIN_EMAIL does not remove the previous user.
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str

    PROJECT_NAME: str = Field(default="Swiple")
    API_VERSION: str = Field(default="/api/v1")

    # "SWIPLE_API" or "SCHEDULER"
    APP: Literal["SWIPLE_API", "SCHEDULER"] = Field(default="SWIPLE_API")
    SWIPLE_API_URL: AnyHttpUrl = Field(default="http://swiple_api:8000")
    UI_URL: AnyHttpUrl = Field(default="http://127.0.0.1:3000")
    SCHEDULER_API_URL: str = Field(default="http://scheduler:8001")
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(default=["http://swiple_api:8000", "http://127.0.0.1:3000"])
    REDIRECT_URL: AnyHttpUrl = "http://127.0.0.1:3000/login"

    # Lifetime of HTTP Cookie
    # Default: 8 hrs
    AUTH_LIFETIME_IN_SECONDS: int = Field(default="28800")
    AUTH_COOKIE_SECURE: bool = True
    USERNAME_AND_PASSWORD_ENABLED: bool = Field(default=True)

    GITHUB_OAUTH_ENABLED: bool = Field(default=False)
    GITHUB_OAUTH_CLIENT_ID: str = Field(default=None)
    GITHUB_OAUTH_SECRET: str = Field(default=None)

    GOOGLE_OAUTH_ENABLED: bool = Field(default=False)
    GOOGLE_OAUTH_CLIENT_ID: str = Field(default=None)
    GOOGLE_OAUTH_SECRET: str = Field(default=None)

    MICROSOFT_OAUTH_ENABLED: bool = Field(default=False)
    MICROSOFT_OAUTH_CLIENT_ID: str = Field(default=None)
    MICROSOFT_OAUTH_SECRET: str = Field(default=None)
    MICROSOFT_OAUTH_TENANT: str = Field(default=None)  # defaults to "common" when not set

    OKTA_OAUTH_ENABLED: bool = Field(default=False)
    OKTA_OAUTH_CLIENT_ID: str = Field(default=None)
    OKTA_OAUTH_SECRET: str = Field(default=None)
    OKTA_OAUTH_BASE_URL: str = Field(default=None)

    SCHEDULER_EXECUTOR_MAX_WORKERS: int = Field(default=10)
    SCHEDULER_EXECUTOR_KWARGS: dict = Field(default=None)
    SCHEDULER_REDIS_DB: int = Field(default=0)

    # list of Redis connection properties e.g. host, port, password
    # https://github.com/redis/redis-py/blob/bedf3c82a55b4b67eed93f686cb17e82f7ab19cd/redis/client.py#L899
    SCHEDULER_REDIS_KWARGS: dict = Field(default={"host": "redis"})

    OPENSEARCH_HOST: str = Field(default="opensearch-node1")
    OPENSEARCH_PORT: str = Field(default="9200")
    OPENSEARCH_USERNAME: str = Field(default="admin")
    OPENSEARCH_PASSWORD: str = Field(default="admin")

    # OpenSearch Index names
    DATASOURCE_INDEX: str = "datasources"
    DATASET_INDEX: str = "datasets"
    EXPECTATION_INDEX: str = "expectations"
    VALIDATION_INDEX: str = "validations"
    SUGGESTION_INDEX: str = "suggestions"
    USER_INDEX: str = "user"

    TOKEN_URL: str = "/api/v1/token"

    class Config:
        env_nested_delimiter = "__"

    @root_validator
    def check_auth_methods(cls, values):
        github_oauth_enabled = values.get("GITHUB_OAUTH_ENABLED")
        google_oauth_enabled = values.get("GOOGLE_OAUTH_ENABLED")
        microsoft_oauth_enabled = values.get("MICROSOFT_OAUTH_ENABLED")
        okta_oauth_enabled = values.get("OKTA_OAUTH_ENABLED")

        username_and_password_enabled = values.get("USERNAME_AND_PASSWORD_ENABLED")

        auth_methods = [github_oauth_enabled, okta_oauth_enabled, username_and_password_enabled]

        if True not in auth_methods:
            raise ValueError("At lease one auth method should be enabled.")

        if github_oauth_enabled:
            github_oauth_client_id = values.get("GITHUB_OAUTH_CLIENT_ID")
            github_oauth_secret = values.get("GITHUB_OAUTH_SECRET")

            if not github_oauth_client_id:
                raise ValueError("GITHUB_OAUTH_CLIENT_ID is required when GITHUB_OAUTH_ENABLED is true.")
            if not github_oauth_secret:
                raise ValueError("GITHUB_OAUTH_SECRET is required when GITHUB_OAUTH_ENABLED is true.")

        if google_oauth_enabled:
            google_oauth_client_id = values.get("GOOGLE_OAUTH_CLIENT_ID")
            google_oauth_secret = values.get("GOOGLE_OAUTH_SECRET")

            if not google_oauth_client_id:
                raise ValueError("GOOGLE_OAUTH_CLIENT_ID is required when GOOGLE_OAUTH_ENABLED is true.")
            if not google_oauth_secret:
                raise ValueError("GOOGLE_OAUTH_SECRET is required when GOOGLE_OAUTH_ENABLED is true.")

        if microsoft_oauth_enabled:
            microsoft_oauth_client_id = values.get("MICROSOFT_OAUTH_CLIENT_ID")
            microsoft_oauth_secret = values.get("MICROSOFT_OAUTH_SECRET")

            if not microsoft_oauth_client_id:
                raise ValueError("MICROSOFT_OAUTH_CLIENT_ID is required when MICROSOFT_OAUTH_ENABLED is true.")
            if not microsoft_oauth_secret:
                raise ValueError("MICROSOFT_OAUTH_SECRET is required when MICROSOFT_OAUTH_ENABLED is true.")

        if okta_oauth_enabled:
            okta_oauth_client_id = values.get("OKTA_OAUTH_CLIENT_ID")
            okta_oauth_secret = values.get("OKTA_OAUTH_SECRET")
            okta_oauth_base_url = values.get("OKTA_OAUTH_BASE_URL")

            if not okta_oauth_client_id:
                raise ValueError("OKTA_OAUTH_CLIENT_ID is required when OKTA_OAUTH_ENABLED is true.")
            if not okta_oauth_secret:
                raise ValueError("OKTA_OAUTH_SECRET is required when OKTA_OAUTH_ENABLED is true.")
            if not okta_oauth_base_url:
                raise ValueError("OKTA_OAUTH_BASE_URL is required when OKTA_OAUTH_ENABLED is true.")

        return values

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
