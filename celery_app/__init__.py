from datetime import timedelta

from celery import Celery

app = Celery('hello', broker='redis://localhost:6379/0',backend='redis://localhost:6379/0')

from celery_app import tasks
from celery.schedules import crontab

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'geg': {
        'task': 'celery_app.tasks.hello',
        'schedule': timedelta(seconds=10),
    },
}

