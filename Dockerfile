FROM python:3.10-slim-bullseye AS builder

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY requirements.txt .

RUN pip install --user -r requirements.txt

FROM python:3.10-slim
WORKDIR /app/

COPY --from=builder /root/.local /root/.local
COPY . /app/

ENV PATH=/root/.local:$PATH
