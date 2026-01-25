# Базовый образ с Python
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /tmp/ai_sidekick

COPY pyproject.toml .python-version ./

RUN uv pip install --system .

COPY app/ ./app/

ENV PYTHONPATH=/tmp/ai_sidekick/app
