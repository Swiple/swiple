from celery import Celery
from kombu.serialization import register
from app.settings import settings


def python_serializer(data):
    return data


def python_deserializer(data):
    return data


# Register the custom serializer with a name, e.g., 'python'
register(
    name='python',
    encoder=python_serializer,
    decoder=python_deserializer,
    content_type='application/x-python',
    content_encoding='utf-8',
)

celery_app = Celery(
    __name__,
    include=[
        'app.worker.tasks.validation',
        'app.worker.tasks.suggestions',
    ],
    result_serializer='python',
    accept_content=['application/json', 'application/x-python'],
    task_track_started=True,
    result_extended=True,
    **settings.SWIPLE_CELERY_CONFIG
)
