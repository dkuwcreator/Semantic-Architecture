#!/bin/bash
# Run tests locally on Linux/macOS

set -e

echo "=== Semantic Architecture MCP Server - Test Runner ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}Using Python ${PYTHON_VERSION}${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements-dev.txt

# Run tests based on argument
TEST_TYPE="${1:-all}"

case "$TEST_TYPE" in
    unit)
        echo -e "${GREEN}Running unit tests...${NC}"
        pytest tests/unit -v --tb=short -m unit
        ;;
    integration)
        echo -e "${GREEN}Running integration tests...${NC}"
        pytest tests/integration -v --tb=short -m integration
        ;;
    semantic)
        echo -e "${GREEN}Running semantic integrity tests...${NC}"
        pytest tests/semantic -v --tb=short -m semantic
        ;;
    coverage)
        echo -e "${GREEN}Running all tests with coverage...${NC}"
        pytest -v --tb=short --cov=mcp_server --cov-report=term-missing --cov-report=html
        echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
        ;;
    quick)
        echo -e "${GREEN}Running quick tests (unit only)...${NC}"
        pytest tests/unit -v --tb=short -x
        ;;
    all)
        echo -e "${GREEN}Running all tests...${NC}"
        pytest -v --tb=short
        ;;
    *)
        echo -e "${RED}Unknown test type: $TEST_TYPE${NC}"
        echo "Usage: $0 [unit|integration|semantic|coverage|quick|all]"
        exit 1
        ;;
esac

# Check exit code
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Tests passed!${NC}"
else
    echo -e "${RED}✗ Tests failed!${NC}"
    exit 1
fi
