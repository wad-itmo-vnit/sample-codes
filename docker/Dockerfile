FROM python:3.8.1-slim-buster

WORKDIR /usr/src/app

RUN pip install --upgrade pip
ADD . /usr/src/app/
RUN pip install -r requirements.txt

CMD [ "python" , "./src/app.py"]