# Multi-stage Dockerfile for Semantic Architecture MCP Server
FROM python:3.12-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY mcp_server/ ./mcp_server/
COPY scripts/ ./scripts/
COPY docs/ ./docs/
COPY data/ ./data/
COPY .github/ ./.github/

# Create non-root user for security
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

USER mcpuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["uvicorn", "mcp_server.main:app", "--host", "0.0.0.0", "--port", "8000"]


# Development stage with hot-reload
FROM base as development

USER root

# Install development dependencies
RUN pip install --no-cache-dir pytest pytest-asyncio httpx

USER mcpuser

# Override CMD for development with reload
CMD ["uvicorn", "mcp_server.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# Production stage (optimized)
FROM base as production

USER mcpuser

# Use multiple workers in production
CMD ["uvicorn", "mcp_server.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
