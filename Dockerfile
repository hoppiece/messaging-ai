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
  poetry config virtualenvs.create false \
  && poetry install --no-root
COPY src src
RUN poetry install


FROM python:3.12-slim-bookworm as runner
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.3 /lambda-adapter /opt/extensions/lambda-adapter
ENV PORT=8000 READINESS_CHECK_PATH=/healthz
RUN \
  apt-get update && apt-get install --no-install-recommends -y \
  libmariadb-dev \
  && apt-get clean && rm -rf /var/lib/apt/lists/*
USER nobody
WORKDIR /app
COPY --from=base \
  --chown=user:nobody:nogroup \
  /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY src/api src/api
WORKDIR /app/src/api
EXPOSE 8000
ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
