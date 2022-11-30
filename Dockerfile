ARG DOCKER_IMAGE=python:3.11-buster
FROM $DOCKER_IMAGE

WORKDIR /app

COPY project/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

WORKDIR /app/project

CMD ["uwsgi", "app.ini"]
