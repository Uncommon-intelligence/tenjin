FROM python:3.9-alpine

RUN apk add --no-cache build-base

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .