#!/bin/bash
# Startup script for Docker deployment

set -e

MODE="${1:-dev}"

echo "🐳 Starting Semantic Architecture MCP Server (Docker Mode)"
echo "=========================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose (support both v1 and v2)
COMPOSE_CMD=""
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker version: $(docker --version)"
echo "✓ Docker Compose: $COMPOSE_CMD"

# Build and start based on mode
if [ "$MODE" == "dev" ]; then
    echo ""
    echo "Starting in DEVELOPMENT mode with hot-reload..."
    echo "=========================================================="
    $COMPOSE_CMD up --build mcp-server-dev
elif [ "$MODE" == "prod" ]; then
    echo ""
    echo "Starting in PRODUCTION mode with multiple workers..."
    echo "=========================================================="
    $COMPOSE_CMD up --build -d mcp-server-prod
    echo ""
    echo "✓ Server started in background"
    echo "  - API: http://localhost:8000"
    echo "  - Docs: http://localhost:8000/docs"
    echo ""
    echo "View logs with: $COMPOSE_CMD logs -f mcp-server-prod"
    echo "Stop server with: $COMPOSE_CMD down"
elif [ "$MODE" == "stop" ]; then
    echo ""
    echo "Stopping all containers..."
    $COMPOSE_CMD down
    echo "✓ Containers stopped"
else
    echo ""
    echo "Usage: $0 [dev|prod|stop]"
    echo "  dev  - Start development server with hot-reload"
    echo "  prod - Start production server in background"
    echo "  stop - Stop all containers"
    exit 1
fi
