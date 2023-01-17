from app.settings import settings
from app.db.client import async_client
from fastapi_users_db_opensearch import OpenSearchUserDatabase
from app.core.users import UserManager
from app.models.users import UserUpdate, UserDB, UserCreate
import asyncio


async def create_admin_user():
    user_db = OpenSearchUserDatabase(UserDB, async_client)
    user_manager = UserManager(user_db)
    user = await user_manager.get_by_email(settings.ADMIN_EMAIL)

    if user is None:
        print("Creating admin user.")
        # Create admin user
        await user_manager.create(
            UserCreate(
                email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD,
                is_superuser=True,
                is_verified=True,
            )
        )
        print("Admin user created")
    else:
        print("Admin user already exists. Updating...")
        user_update = UserUpdate(
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD,
            is_superuser=True,
            is_active=True,
        )
        await user_manager.update(
            user_update=user_update,
            user=user,
        )
        print("Admin user updated.")


asyncio.run(create_admin_user())
