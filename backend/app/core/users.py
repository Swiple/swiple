from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy
from fastapi_users.manager import UserAlreadyExists
from fastapi_users_db_opensearch import OpenSearchUserDatabase
from pydantic import EmailStr

from app.db.client import get_user_db, async_client
from app.models.auth import User, UserCreate, UserDB, UserUpdate
from app.config.settings import settings

SECRET = settings.SECRET_KEY


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: UserDB, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: UserDB, token: str, request: Optional[Request] = None):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        return token


def get_user_manager(user_db: OpenSearchUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=settings.AUTH_LIFETIME_IN_SECONDS)


cookie_transport = CookieTransport(
    cookie_name="swipleuserauth",
    cookie_max_age=settings.AUTH_LIFETIME_IN_SECONDS,
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


async def create_user(email: EmailStr, password: str, is_superuser: bool = False):
    try:
        user_db = OpenSearchUserDatabase(UserDB, async_client)
        user_manager = UserManager(user_db)
        try:
            user = await user_manager.create(
                UserCreate(
                    email=email, password=password, is_superuser=is_superuser
                )
            )
            print(f"User created {user.email}")

        except UserAlreadyExists:
            print(f"User {email} already exists. Updating user.")
            user_update = UserUpdate(
                email=email, password=password, is_superuser=is_superuser
            )
            user = await user_manager.get_by_email(user_email=email)
            await user_manager.update(
                user_update=user_update,
                user=user,
            )
    except Exception as ex:
        print(ex)
