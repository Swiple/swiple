from fastapi import APIRouter
from fastapi.params import Depends
from app.core.users import current_active_user
from app.models.task import TaskReadyResponse, TaskResultResponse
from app.repositories.task import TaskRepository, get_task_repository
from app.worker.app import celery_app


router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("/{task_id}", response_model=TaskResultResponse)
def get_task(
    task_id: str,
    repository: TaskRepository = Depends(get_task_repository),
):
    return repository.get(task_id)


@router.get("/{task_id}/ready", response_model=TaskReadyResponse)
def get_task_ready(task_id: str):
    is_ready = celery_app.AsyncResult(task_id).ready()
    return {"is_ready": is_ready}
