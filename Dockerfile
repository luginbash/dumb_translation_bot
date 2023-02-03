FROM python:3.10-bullseye

MAINTAINER Luginbash Hiyajo <725033+luginbash@users.noreply.github.com>

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD /app/app.py

