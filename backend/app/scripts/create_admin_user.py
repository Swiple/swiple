import asyncio

from app.core.users import create_user
from app.settings import settings


async def create_admin_user():
    # Create admin user
    await create_user(
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD,
        is_superuser=True,
    )


asyncio.run(create_admin_user())
