from typing import Any, Optional

from app.models.users import User
from app.repositories.base import BaseRepository, get_repository
from app.settings import settings


class UserRepository(BaseRepository[User]):
    model_class = User
    index = settings.USER_INDEX

    def _get_object_from_dict(self, d: dict[str, Any], *, id: Optional[str] = None) -> User:
        if id is not None:
            d["id"] = id
        return User.parse_obj(d)


get_user_repository = get_repository(UserRepository)
