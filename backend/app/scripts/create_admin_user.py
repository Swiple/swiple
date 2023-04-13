import fastapi_users.manager

from app.settings import settings
from app.core.users import get_user_db, get_user_manager
from app.models.users import AdminUserCreate, AdminUserUpdate
import asyncio


async def create_admin_user():
    user_db = get_user_db()
    user_manager = get_user_manager(user_db)
    try:
        user = await user_manager.get_by_email(settings.ADMIN_EMAIL)

        print("Admin user already exists. Updating...")
        user_update = AdminUserUpdate(
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD,
            is_superuser=True,
            is_active=True,
            is_admin_user=True,
        )
        await user_manager.update(
            user_update=user_update,
            user=user,
            allow_admin_update=True,
        )
        print("Admin user updated.")
    except fastapi_users.manager.UserNotExists:
        print("Creating admin user.")
        # Create admin user
        await user_manager.create(
            AdminUserCreate(
                email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD,
                is_superuser=True,
                is_verified=True,
                is_admin_user=True,
            )
        )
        print("Admin user created")
    finally:
        await user_db.client.close()


if __name__ == '__main__':
    asyncio.run(create_admin_user())
