FROM python:3.10.7-slim

ARG ENV
ARG SRC_DIR=canvass_api_model_store

ENV ENV=${ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=true \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_NO_INTERACTION=1 \
  POETRY_NO_ANSI=1 \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PYTHONPATH="$PYTHONPATH:/app/${SRC_DIR}"

RUN apt-get update &&  \
    apt-get install -y  \
      libpq-dev  \
      gcc  \
      git &&  \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy entrypoint.sh and start.sh to /usr/local/bin
COPY ./scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN sed -i 's/\r$//g' /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY ./scripts/start.sh /usr/local/bin/start.sh
RUN sed -i 's/\r$//g' /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /app

# Download public key for github.com
RUN --mount=type=ssh mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

COPY pyproject.toml poetry.lock* ./
RUN --mount=type=ssh \
    poetry install $(test "$ENV" = production && echo "--without dev")

COPY ${SRC_DIR}/ ${SRC_DIR}/

ENTRYPOINT ["entrypoint.sh"]
