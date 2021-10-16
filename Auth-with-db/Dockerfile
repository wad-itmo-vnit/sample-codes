FROM python:3.8.1-slim-buster

WORKDIR /usr/src/app

RUN pip install --upgrade pip
ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt