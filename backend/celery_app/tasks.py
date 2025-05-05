from backend.celery_app import app


@app.task
def hello():
    return "hello world"


# celery -A celery_app beat
# docker run -d -p 6379:6379 redis
# celery -A myproject worker --loglevel=info -P gevent
