FROM python:3.8-slim-buster

# django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./core .
EXPOSE 8000

# nginx
RUN apt-get update && apt-get install -y nginx
COPY /hamravesh/product/backend/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80

# entrypoint
COPY /hamravesh/product/backend/entrypoint.sh .
RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]