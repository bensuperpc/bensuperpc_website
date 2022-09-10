ARG DOCKER_IMAGE=python:3.10-buster
FROM $DOCKER_IMAGE

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ARG flask_app=project
ENV FLASK_APP $flask_app

EXPOSE 5000

CMD ["make", "run"]