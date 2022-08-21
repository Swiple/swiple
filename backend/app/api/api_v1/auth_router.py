from fastapi import APIRouter, Depends
from httpx_oauth.clients.github import GitHubOAuth2
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.microsoft import MicrosoftGraphOAuth2
from httpx_oauth.clients.okta import OktaOAuth2
from app.core.users import fastapi_users, cookie_backend, current_active_superuser
from app.settings import settings

router = APIRouter()
router.include_router(
    fastapi_users.get_users_router(),
    prefix="/user",
    tags=["Users"]
)

if settings.USERNAME_AND_PASSWORD_ENABLED:
    # Username + Password
    router.include_router(
        fastapi_users.get_auth_router(cookie_backend),
        prefix="/auth",
        tags=["Auth"],
    )

    router.include_router(
        fastapi_users.get_register_router(),
        prefix="/auth",
        tags=["Auth"],
        dependencies=[Depends(current_active_superuser)]
    )
    router.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["Auth"],
    )
    router.include_router(
        fastapi_users.get_verify_router(),
        prefix="/auth",
        tags=["Auth"],
    )

if settings.GITHUB_OAUTH_ENABLED:
    # GitHub OAuth
    github_oauth_client = GitHubOAuth2(settings.GITHUB_OAUTH_CLIENT_ID, settings.GITHUB_OAUTH_SECRET)

    router.include_router(
        fastapi_users.get_oauth_router(
            backend=cookie_backend,
            oauth_client=github_oauth_client,
            state_secret=github_oauth_client.client_secret,
            redirect_url=f"{settings.REDIRECT_URL}?provider=github",
        ),
        prefix="/auth/github",
        tags=["Auth"],
    )

if settings.GOOGLE_OAUTH_ENABLED:
    # Google OAuth
    google_oauth_client = GoogleOAuth2(settings.GOOGLE_OAUTH_CLIENT_ID, settings.GOOGLE_OAUTH_SECRET)

    router.include_router(
        fastapi_users.get_oauth_router(
            backend=cookie_backend,
            oauth_client=google_oauth_client,
            state_secret=google_oauth_client.client_secret,
            redirect_url=f"{settings.REDIRECT_URL}?provider=google",
        ),
        prefix="/auth/google",
        tags=["Auth"],
    )

if settings.MICROSOFT_OAUTH_ENABLED:
    # Microsoft OAuth
    microsoft_oauth_client = MicrosoftGraphOAuth2(
        settings.MICROSOFT_OAUTH_CLIENT_ID,
        settings.MICROSOFT_OAUTH_SECRET,
        settings.MICROSOFT_OAUTH_TENANT
    )

    router.include_router(
        fastapi_users.get_oauth_router(
            backend=cookie_backend,
            oauth_client=microsoft_oauth_client,
            state_secret=microsoft_oauth_client.client_secret,
            redirect_url=f"{settings.REDIRECT_URL}?provider=microsoft",
        ),
        prefix="/auth/microsoft",
        tags=["Auth"],
    )

if settings.OKTA_OAUTH_ENABLED:
    # Okta OAuth
    okta_oauth_client = OktaOAuth2(
        settings.OKTA_OAUTH_CLIENT_ID,
        settings.OKTA_OAUTH_SECRET,
        settings.OKTA_OAUTH_BASE_URL
    )

    router.include_router(
        fastapi_users.get_oauth_router(
            backend=cookie_backend,
            oauth_client=okta_oauth_client,
            state_secret=okta_oauth_client.client_secret,
            redirect_url=f"{settings.REDIRECT_URL}?provider=okta",
        ),
        prefix="/auth/okta",
        tags=["Auth"],
    )
