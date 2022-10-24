ARG DOCKER_IMAGE=python:3.10-buster
FROM $DOCKER_IMAGE

WORKDIR /app

COPY project/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "wsgi.py"]