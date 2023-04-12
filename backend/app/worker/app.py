from celery import Celery
from app.settings import settings


celery_app = Celery(
    __name__,
    include=[
        'app.worker.tasks.validation',
        'app.worker.tasks.suggestions',
    ],
    accept_content=['application/json'],
    task_track_started=True,
    result_extended=True,
    **settings.SWIPLE_CELERY_CONFIG
)
