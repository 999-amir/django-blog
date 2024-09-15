FROM python:3.8-slim-buster

# django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./core .

CMD python3 manage.py collectstatic --no-input
