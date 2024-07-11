FROM python:3.10-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt
