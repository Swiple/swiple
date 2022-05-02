from typing import List, Union
from pydantic import AnyHttpUrl, HttpUrl, BaseSettings, EmailStr, validator, root_validator
from app.config import config


class Settings(BaseSettings):
    PROJECT_NAME: str = config.PROJECT_NAME
    API_VERSION: str = config.API_VERSION

    AUTH_LIFETIME_IN_SECONDS: int = config.AUTH_LIFETIME_IN_SECONDS
    SECRET_KEY: str = config.SECRET_KEY

    USERNAME_AND_PASSWORD_ENABLED: bool = config.USERNAME_AND_PASSWORD_ENABLED
    ADMIN_EMAIL: EmailStr = config.ADMIN_EMAIL
    ADMIN_PASSWORD: str = config.ADMIN_PASSWORD

    GITHUB_OAUTH_ENABLED: bool = config.GITHUB_OAUTH_ENABLED
    GITHUB_OAUTH_CLIENT_ID: str = config.GITHUB_OAUTH_CLIENT_ID
    GITHUB_OAUTH_SECRET: str = config.GITHUB_OAUTH_SECRET

    GOOGLE_OAUTH_ENABLED: bool = config.GOOGLE_OAUTH_ENABLED
    GOOGLE_OAUTH_CLIENT_ID: str = config.GOOGLE_OAUTH_CLIENT_ID
    GOOGLE_OAUTH_SECRET: str = config.GOOGLE_OAUTH_SECRET

    MICROSOFT_OAUTH_ENABLED: bool = config.MICROSOFT_OAUTH_ENABLED
    MICROSOFT_OAUTH_CLIENT_ID: str = config.MICROSOFT_OAUTH_CLIENT_ID
    MICROSOFT_OAUTH_SECRET: str = config.MICROSOFT_OAUTH_SECRET
    MICROSOFT_OAUTH_TENANT: str = config.MICROSOFT_OAUTH_TENANT

    OKTA_OAUTH_ENABLED: bool = config.OKTA_OAUTH_ENABLED
    OKTA_OAUTH_CLIENT_ID: str = config.OKTA_OAUTH_CLIENT_ID
    OKTA_OAUTH_SECRET: str = config.OKTA_OAUTH_SECRET
    OKTA_OAUTH_BASE_URL: str = config.OKTA_OAUTH_BASE_URL

    OPENSEARCH_HOST: str = config.OPENSEARCH_HOST
    OPENSEARCH_PORT: str = config.OPENSEARCH_PORT
    OPENSEARCH_USERNAME: str = config.OPENSEARCH_USERNAME
    OPENSEARCH_PASSWORD: str = config.OPENSEARCH_PASSWORD

    # OpenSearch Index names
    DATASOURCE_INDEX: str = "datasource"
    DATASET_INDEX: str = "dataset"
    EXPECTATION_INDEX: str = "expectation"
    VALIDATION_INDEX: str = "validation"
    SUGGESTION_INDEX: str = "suggestion"
    USER_INDEX: str = "user"

    TOKEN_URL: str = "/api/v1/token"
    API_HOST_URL: HttpUrl = config.API_HOST_URL
    UI_HOST_URL: HttpUrl = config.UI_HOST_URL
    REDIRECT_URL: HttpUrl = f"{UI_HOST_URL}/login"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = config.BACKEND_CORS_ORIGINS

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
