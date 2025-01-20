FROM python:3.12-slim

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME=/usr

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml .
RUN poetry install --no-ansi --no-root

COPY src /code
WORKDIR /code
ENTRYPOINT [ "sleep" ,  "infinity" ]

