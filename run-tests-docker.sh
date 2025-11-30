#!/bin/bash
# Run tests in Docker containers

set -e

echo "=== Semantic Architecture MCP Server - Docker Test Runner ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: docker-compose is not installed${NC}"
    exit 1
fi

# Determine docker compose command
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo -e "${GREEN}Using Docker Compose${NC}"

# Run tests based on argument
TEST_TYPE="${1:-all}"

case "$TEST_TYPE" in
    build)
        echo -e "${YELLOW}Building test containers...${NC}"
        $DOCKER_COMPOSE -f docker-compose.test.yml build
        ;;
    unit)
        echo -e "${GREEN}Running unit tests in Docker...${NC}"
        $DOCKER_COMPOSE -f docker-compose.test.yml run --rm test pytest tests/unit -v --tb=short -m unit
        ;;
    integration)
        echo -e "${GREEN}Running integration tests in Docker...${NC}"
        $DOCKER_COMPOSE -f docker-compose.test.yml up --abort-on-container-exit integration-test
        ;;
    all)
        echo -e "${GREEN}Running all tests in Docker...${NC}"
        $DOCKER_COMPOSE -f docker-compose.test.yml run --rm test
        ;;
    server)
        echo -e "${GREEN}Starting MCP server for testing...${NC}"
        $DOCKER_COMPOSE -f docker-compose.test.yml up mcp-server
        ;;
    clean)
        echo -e "${YELLOW}Cleaning up Docker resources...${NC}"
        $DOCKER_COMPOSE -f docker-compose.test.yml down -v
        docker system prune -f
        ;;
    coverage)
        echo -e "${GREEN}Running tests with coverage in Docker...${NC}"
        $DOCKER_COMPOSE -f docker-compose.test.yml run --rm test pytest -v --tb=short --cov=mcp_server --cov-report=term-missing --cov-report=html:/app/htmlcov
        echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
        ;;
    *)
        echo -e "${RED}Unknown test type: $TEST_TYPE${NC}"
        echo "Usage: $0 [build|unit|integration|all|server|clean|coverage]"
        exit 1
        ;;
esac

# Check exit code
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Docker tests completed!${NC}"
else
    echo -e "${RED}✗ Docker tests failed!${NC}"
    exit 1
fi
