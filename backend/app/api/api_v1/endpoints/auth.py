from app.settings import settings
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/methods")
def methods():
    enabled_auth_methods = []

    if settings.USERNAME_AND_PASSWORD_ENABLED:
        enabled_auth_methods.append("username_and_password")
    if settings.GITHUB_OAUTH_ENABLED:
        enabled_auth_methods.append("github")
    if settings.GOOGLE_OAUTH_ENABLED:
        enabled_auth_methods.append("google")
    if settings.MICROSOFT_OAUTH_ENABLED:
        enabled_auth_methods.append("microsoft")
    if settings.OKTA_OAUTH_ENABLED:
        enabled_auth_methods.append("okta")

    return JSONResponse(status_code=status.HTTP_200_OK, content=enabled_auth_methods)
