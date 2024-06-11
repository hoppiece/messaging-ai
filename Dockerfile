FROM python:3.12-bookworm as base
WORKDIR /app
RUN \
  --mount=type=cache,target=/var/cache/apt \
  apt-get update && apt-get install --no-install-recommends -y \
  libmariadb-dev
RUN \
  --mount=type=cache,target=/root/.cache/pip \
  pip install poetry==1.8.3
COPY README.md ./pyproject.toml ./poetry.lock* ./
RUN \
  --mount=type=cache,target=/root/.cache/pypoetry \
  poetry config virtualenvs.in-project true \
  && poetry config virtualenvs.options.always-copy true \
  && poetry config virtualenvs.options.no-setuptools true \
  && poetry install --no-root
COPY src src
RUN poetry install


FROM python:3.12-slim-bookworm as runner-base
RUN \
  apt-get update && apt-get install --no-install-recommends -y \
  libmariadb-dev \
  && apt-get clean && rm -rf /var/lib/apt/lists/*
USER nobody
WORKDIR /app
COPY \
  --from=base \
  --chown=user:nobody:nogroup \
  /app/.venv/ /venv/
COPY src/api src/api
WORKDIR /app/src/api
EXPOSE 8000
ENTRYPOINT ["/venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM runner-base as runner-lambda
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.3 /lambda-adapter /opt/extensions/lambda-adapter
ENV PORT 8000
ENV READINESS_CHECK_PATH /healthz
