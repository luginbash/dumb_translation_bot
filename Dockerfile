ARG VERSION

FROM python:3.10-bullseye

MAINTAINER Luginbash Hiyajo <bash@lug.sh>

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD /app/app.py

