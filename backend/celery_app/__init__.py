from datetime import timedelta
from celery import Celery
from celery.schedules import crontab

app = Celery(
    "hello", broker="redis://localhost:6380/0", backend="redis://localhost:6380/0"
)

from backend.celery_app import tasks

app.conf.beat_schedule = {

    "parser": {
        "task": "backend.celery_app.tasks.parser",
        "schedule": crontab(minute=45),
    },
}

# Возможный вариант для времени

# app.conf.beat_schedule = {
#
#     "parser": {
#         "task": "backend.celery_app.tasks.parser",
#         "schedule": crontab(minute=0, hour=7, day_of_week=2),
#     },
# }