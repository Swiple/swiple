from fastapi_users import models


class User(models.BaseUser):
    is_admin_user: bool = False


class AdminUserCreate(models.BaseUserCreate):
    is_admin_user: bool = False


class AdminUserUpdate(models.BaseUserUpdate):
    is_admin_user: bool = False


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    is_admin_user: bool = False
