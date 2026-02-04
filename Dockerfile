FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Separate for caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --compile-bytecode

FROM python:3.13-slim

WORKDIR /app

RUN useradd -m myuser && chown myuser:myuser /app
USER myuser

COPY --chown=myuser:myuser --from=builder /app/.venv /app/.venv
COPY --chown=myuser:myuser . .

ENV PATH="/app/.venv/bin:$PATH"

RUN mkdir -p output && python train_model.py

# Default env vars
ENV PORT=8050
ENV HOST=0.0.0.0

CMD ["uvicorn", "fast_api:app", "--host", "0.0.0.0", "--port", "8050"]
