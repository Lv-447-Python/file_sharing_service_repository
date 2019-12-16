#FROM alpine:3.8
#RUN apk add --no-cache python3 \
#    && apk add python3-dev \
#    && apk add postgresql-dev gcc python3-dev musl-dev \
#    && python3 -m ensurepip \
#    && rm -r /usr/lib/python*/ensurepip\
#    && mkdir /file_sharing_service

#FROM ubuntu:18.04
#RUN apt-get update \
#    && apt-get install -y python3 python3-dev python3-pip libpq-dev
#    && mkdir /file_sharing_service

#VOLUME /file_sharing_service
#WORKDIR /file_sharing_service
#COPY requirements.txt /file_sharing_service
#RUN pip3 install -r requirements.txt
#COPY . /file_sharing_service
#EXPOSE 5000
#CMD ["python3", "app.py"]

FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]
