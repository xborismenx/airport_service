FROM python:3.12-alpine3.20

LABEL maintainer="boris.tikhonov.21"

ENV PYTHONUNBUFFERED=1

WORKDIR /app


RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
