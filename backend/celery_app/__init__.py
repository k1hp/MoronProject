from datetime import timedelta

from celery import Celery

app = Celery(
    "hello", broker="redis://localhost:6380/0", backend="redis://localhost:6380/0"
)

from backend.celery_app import tasks

app.conf.beat_schedule = {

    "geg": {
        "task": "backend.celery_app.tasks.parser",
        "schedule": timedelta(seconds=200),
    },
}
