FROM --platform=arm64 python:3.11

RUN apt-get -y update

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .