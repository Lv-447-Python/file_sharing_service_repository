FROM python:3.8.1-alpine3.10

WORKDIR /file_sharing_service
RUN mkdir $WORKDIR/file_sharing_service/generated_files

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add bash \
    && apk add make 
#    && pip install --upgrade pip


COPY requirements.txt /file_sharing_service/requirements.txt
RUN pip install -r requirements.txt

COPY . /file_sharing_service



#COPY requirements.txt /file_sharing_service
#RUN pip3 install -r requirements.txt
#COPY . /file_sharing_service
#EXPOSE 5000
#CMD ["python3", "app.py"]
#CMD ["make"]