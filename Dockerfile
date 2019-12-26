FROM python:3.7.0-alpine

WORKDIR /file_sharing_service

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add bash \
    && apk add make \
    && pip install --upgrade pip


COPY requirements.txt /file_sharing_service/requirements.txt
RUN pip install -r requirements.txt

COPY . /file_sharing_service
