from fastapi import APIRouter, Depends, HTTPException, status

from fastapi_users.manager import (
    InvalidPasswordException,
    UserAlreadyExists,
)
from fastapi_users.router.common import ErrorCode, ErrorModel

from app.core import users
from app.models.users import User, UserCreate
from app.repositories.user import UserRepository, get_user_repository

router = APIRouter(
    dependencies=[Depends(users.current_active_user)]
)


@router.get("", response_model=list[User])
def list_users(
        repository: UserRepository = Depends(get_user_repository),
):
    return repository.query({"query": {"match_all": {}}}, size=1000)


@router.post(
    "",
    response_model=User,
    dependencies=[Depends(users.current_active_superuser)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The user does not exist.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "detail": ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                            },
                        },
                        ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": {
                                    "reason": "Password should be"
                                    "at least 12 characters",
                                }
                            },
                        },
                    }
                }
            },
        },
    },
)
async def create_user(
    user: UserCreate,
):
    try:
        return await users.create_user(
            email=user.email,
            password=user.password,
            is_superuser=user.is_superuser,
            is_verified=True
        )
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.reason
        )
    except UserAlreadyExists:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="A user with this email address already exists.",
        )
