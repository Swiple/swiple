from fastapi import APIRouter
from fastapi.params import Depends

from app.core.users import current_active_user
from app.models.users import User
from app.repositories.user import UserRepository, get_user_repository

router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("", response_model=list[User])
def users(
        repository: UserRepository = Depends(get_user_repository),
):
    return repository.query({"query": {"match_all": {}}}, size=1000)
