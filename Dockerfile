# Multi-stage Dockerfile for Semantic Architecture tooling + tests (non-server)
FROM python:3.12-slim as base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/
COPY docs/ ./docs/
COPY data/ ./data/
COPY .github/ ./.github/

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser


FROM base as testing

USER root

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY tests/ ./tests/
COPY pytest.ini .

RUN chown -R appuser:appuser /app
USER appuser

CMD ["pytest", "-v", "--tb=short"]
