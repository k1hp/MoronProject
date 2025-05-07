FROM python:3.12

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .


CMD ["celery", "-A", "backend.celery_app", "beat", "--loglevel=info"]