FROM certbot/certbot:v1.27.0

COPY /dockerfiles/product/certbot/certify-init.sh /opt/
RUN chmod +x /opt/certify-init.sh

ENTRYPOINT []
CMD ["certbot", "renew"]
