FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./core /app

# create non-root user for celery
RUN apt-get update && apt-get install -y libcap2-bin passwd && rm -rf /var/lib/apt/lists/*
RUN useradd --system --create-home --shell /bin/bash celery_user
RUN chown -R celery_user:celery_user /usr/local/lib/python3.8/site-packages
USER celery_user
