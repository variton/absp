FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/

WORKDIR /absp

COPY pyproject.toml  ./

RUN uv pip install --system black coverage

COPY src/ ./src/