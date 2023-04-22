from app.core.runner import run_dataset_validation
from app.worker.app import celery_app
from app.db.client import client
from app.settings import settings
from uuid import uuid4
from celery import current_task


@celery_app.task(name="validation.run")
def run_validation(*, dataset_id: str):
    task_id = current_task.request.id
    validation = run_dataset_validation(dataset_id, task_id)
    client.index(
        index=settings.VALIDATION_INDEX,
        id=str(uuid4()),
        body=validation.dict(),
        refresh="wait_for",
    )
