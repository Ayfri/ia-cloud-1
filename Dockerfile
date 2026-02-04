FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Separate for caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --compile-bytecode

FROM python:3.13-slim

WORKDIR /app

RUN useradd -m myuser
USER myuser

COPY --from=builder /app/.venv /app/.venv

COPY app ./app

ENV PATH="/app/.venv/bin:$PATH"

# Default env vars
ENV PORT=8050
ENV HOST=0.0.0.0

CMD uvicorn app.main:app --host $HOST --port $PORT
