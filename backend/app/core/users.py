import re
from typing import Optional, Union
from fastapi import Depends, Request, HTTPException, status
from fastapi_users import BaseUserManager, FastAPIUsers, models
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy
from fastapi_users.manager import InvalidPasswordException
from fastapi_users_db_opensearch import OpenSearchUserDatabase

from app.db.client import async_client
from app.models.users import User, UserCreate, UserDB, UserUpdate
from app.settings import settings

SECRET = settings.SECRET_KEY


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def validate_password(
        self, password: str, user: Union[models.UC, models.UD]
    ) -> None:
        if len(password) < 12:
            raise InvalidPasswordException("Password should be at least 12 characters long")

        if not re.search("[A-Z]", password):
            raise InvalidPasswordException("Expect at least 1 uppercase character")

        if not re.search("[0-9]", password):
            raise InvalidPasswordException("Expect at least 1 number")

        if not re.search("[!@#\$%^&*\(\)]", password):
            raise InvalidPasswordException("Expect at least 1 special character")

        return None

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: UserDB, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: UserDB, token: str, request: Optional[Request] = None):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        return token

    async def delete(self, user: models.UD) -> None:
        """
        Delete a user.

        :param user: The user to delete.
        """
        if user.email == settings.ADMIN_EMAIL:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Deleting the admin user is forbidden."
            )
        return await super().delete(user)

    async def update(
        self,
        user_update: models.UU,
        user: models.UD,
        safe: bool = False,
        request: Optional[Request] = None,
        **kwargs,
    ) -> models.UD:
        """
        Update a user.

        Triggers the on_after_update handler on success

        :param user_update: The UserUpdate model containing
        the changes to apply to the user.
        :param user: The current user to update.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the update, defaults to False
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :param kwargs: Additional keyword arguments that can be passed. Currently supports:
            - "allow_admin_update" (bool): If set to True, allows updating the admin user,
            otherwise updating the admin user is forbidden. Defaults to False.
        :return: The updated user.
        """
        allow_admin_update = kwargs.get("allow_admin_update", False)

        if not allow_admin_update and user.email == settings.ADMIN_EMAIL:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Updating the admin user is forbidden."
            )
        return await super().update(user_update, user, safe, request)


def get_user_db():
    from fastapi_users_db_opensearch import OpenSearchUserDatabase

    return OpenSearchUserDatabase(
        UserDB,
        async_client,
        settings.USER_INDEX,
    )


def get_user_manager(user_db: OpenSearchUserDatabase = Depends(get_user_db)):
    return UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=settings.AUTH_LIFETIME_IN_SECONDS)


cookie_transport = CookieTransport(
    cookie_name="swipleuserauth",
    cookie_max_age=settings.AUTH_LIFETIME_IN_SECONDS,
    cookie_secure=settings.AUTH_COOKIE_SECURE,
)

cookie_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers(
    get_user_manager,
    [cookie_backend],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
