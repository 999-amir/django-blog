FROM nginx:alpine

COPY /dockerfiles/product/nginx/config/* /etc/nginx/
COPY /dockerfiles/product/nginx/entrypoint.sh /entrypoint.sh

USER root

RUN apk update && apk add --no-cache bash openssl
RUN chmod +x /entrypoint.sh


CMD ["/entrypoint.sh"]