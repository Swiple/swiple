from app.core.exceptions import SecretsModuleNotFoundError, SecretsKeyError, SecretClientError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request


async def secrets_import_exception_handler(request: Request, exc: SecretsModuleNotFoundError):
    return JSONResponse(
        status_code=422,
        content={
            "message": f"{exc.msg}. Go to https://swiple.io/docs/configuration/secrets-manager for instructions."
        },
    )


async def secrets_key_exception_handler(request: Request, exc: SecretsKeyError):
    return JSONResponse(
        status_code=422,
        content={
            "message": f"Key {exc} does not exist."
        },
    )


async def secret_client_exception_handler(request: Request, exc: SecretClientError):
    return JSONResponse(
        status_code=422,
        content={
            "message": exc.__str__()
        },
    )


def add(app: FastAPI):
    app.add_exception_handler(SecretsModuleNotFoundError, secrets_import_exception_handler)
    app.add_exception_handler(SecretsKeyError, secrets_key_exception_handler)
    app.add_exception_handler(SecretClientError, secret_client_exception_handler)
