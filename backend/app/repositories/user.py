from app.models.users import User
from app.repositories.base import BaseRepository, get_repository
from app.settings import settings


class UserRepository(BaseRepository[User]):
    model_class = User
    index = settings.USER_INDEX


get_user_repository = get_repository(UserRepository)
