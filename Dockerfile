# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY api_objects.py api_objects.py
COPY templates templates/

ENV FLASK_APP=api_objects

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
