from app.settings import settings
from app.core.users import create_user
import asyncio


async def create_admin_user():
    # Create admin user
    await create_user(
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD,
        is_superuser=True,
    )


asyncio.run(create_admin_user())
