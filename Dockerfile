MAINTAINER Luginbash Hiyajo <725033+luginbash@users.noreply.github.com>

FROM python:3.11-bullseye as base
ENV PYTHONUNBUFFERED=1

FROM base as builder
ENV PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1
WORKDIR /build
COPY . /build
RUN pip install poetry && poetry build && poetry install && poetry install dist/*.whl


FROM base as final
WORKDIR /app
COPY --from=build /build/.venv /app
COPY entrypoint.sh ./
CMD ["./docker-entrypoint.sh"]

