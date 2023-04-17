# Utilizamos una imagen de Python 3.9 como base
FROM python:3.9

WORKDIR /app
COPY mqtt2strapi /app
COPY entrypoint.sh /app

RUN pip install -r mqtt2strapi/requirements.txt && \
    chmod +x entrypoint.sh && \
    mkdir /app/config


ENTRYPOINT ["./entrypoint.sh"]
