from typing import Any, Optional
from app.repositories.base import BaseRepository, get_repository
from app.settings import settings
from app.models.task import TaskResult
from app.repositories.base import NotFoundError, OSNotFoundError
from app.worker.app import celery_app


class TaskRepository(BaseRepository[TaskResult]):
    model_class = TaskResult
    index = settings.CELERY_INDEX
    id_prefix = "celery-task-meta-"

    def get(self, id: str) -> TaskResult:
        try:
            task = celery_app.AsyncResult(id)
        except OSNotFoundError as e:
            raise NotFoundError() from e

        return self._get_object_from_dict({
            "task_id": task.task_id,
            "status": task.state,
            "kwargs": task.kwargs,
            "result": task.result,
            "date_done": task.date_done,
        })

    def query_by_dataset_id(self, dataset_id: str, status=None) -> list[TaskResult]:
        # Construct the must array
        must = [{"match": {"result.kwargs.dataset_id.keyword": dataset_id}}]

        # Conditionally add the status match
        if status:
            must.append({"match": {"result.status.keyword": status}})

        return self.query({
            "query": {
                "bool": {
                    "must": must
                }
            }
        })

    def _get_object_from_dict(self, d: dict[str, Any], *, id: Optional[str] = None) -> TaskResult:
        print(d)
        result = d["result"]
        if id is not None:
            result["task_id"] = id.replace(self.id_prefix, "")
        return self.model_class.parse_obj(result)


get_task_repository = get_repository(TaskRepository)
