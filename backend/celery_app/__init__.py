from datetime import timedelta

from celery import Celery

app = Celery("parser", broker="redis:6379", backend="redis:6379")


app.conf.timezone = 'Europe/Moscow'

from backend.celery_app import tasks

app.conf.beat_schedule = {

    "parser": {
        "task": "backend.celery_app.tasks.parser",
        "schedule": timedelta(minutes=10)
    }

}

