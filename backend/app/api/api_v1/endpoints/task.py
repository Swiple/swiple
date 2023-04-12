from fastapi import APIRouter
from fastapi.params import Depends
from app.core.users import current_active_user
from app.models.task import TaskResultResponse
from app.repositories.task import TaskRepository, get_task_repository


router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("/{task_id}", response_model=TaskResultResponse)
def get_task(
    task_id: str,
    repository: TaskRepository = Depends(get_task_repository),
):
    return repository.get(task_id)
