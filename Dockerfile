
FROM python:3.12-alpine as base
MAINTAINER Luginbash Hiyajo <725033+luginbash@users.noreply.github.com>

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1

WORKDIR /builder
COPY . /builder

RUN apk --no-cache add --virtual .build-deps build-base icu-dev \
    && pip install poetry && poetry build && poetry install \
    && apk del .build-deps && apk add py3-icu

CMD ["/builder/.venv/bin/telegram-dumb-translate-bot"]

