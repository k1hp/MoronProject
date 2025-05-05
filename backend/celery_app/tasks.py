from backend.celery_app import app
from backend.parser.parser_dns import parse_processors

@app.task
def parser():
    return parse_processors()



# docker run -d -p 6379:6379 redis
# celery -A celery_app beat
# celery -A myproject worker --loglevel=info -P gevent