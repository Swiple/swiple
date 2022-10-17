from app.core.exceptions import (
    SecretsModuleNotFoundError,
    SecretsKeyError,
    SecretClientError,
    NoCredentialsError
)
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status


async def secrets_import_exception_handler(request: Request, exc: SecretsModuleNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": f"{exc.__str__()}. Go to https://swiple.io/docs/configuration/secrets-manager for instructions."
        },
    )


async def secrets_key_exception_handler(request: Request, exc: SecretsKeyError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": f"Key {exc.__str__()} does not exist."
        },
    )


async def secret_client_exception_handler(request: Request, exc: SecretClientError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": exc.__str__()
        },
    )


async def no_credentials_exception_handler(request: Request, exc: NoCredentialsError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": f"{exc.__str__()}. Swiple has not been given the permissions needed to access secrets."
        },
    )


def add(app: FastAPI):
    app.add_exception_handler(SecretsModuleNotFoundError, secrets_import_exception_handler)
    app.add_exception_handler(SecretsKeyError, secrets_key_exception_handler)
    app.add_exception_handler(SecretClientError, secret_client_exception_handler)
    app.add_exception_handler(NoCredentialsError, no_credentials_exception_handler)
