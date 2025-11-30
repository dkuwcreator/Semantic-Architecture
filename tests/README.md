# Semantic Architecture MCP Server - Testing Suite

This directory contains a comprehensive testing suite for the Semantic Architecture MCP Server, designed to work cross-platform on Linux, macOS, and Windows.

## Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Running Tests Locally](#running-tests-locally)
- [Running Tests in Docker](#running-tests-in-docker)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Test Categories](#test-categories)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

## Overview

The testing suite includes:

- **Unit Tests**: Fast, isolated tests for individual components (models, adapters, utilities)
- **Integration Tests**: Tests for FastAPI endpoints and service integration
- **Semantic Integrity Tests**: Tests for semantic consistency, data integrity, and cross-environment behavior

All tests are designed to run consistently across Linux, macOS, and Windows environments, both locally and in Docker containers.

## Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── conftest.py                    # Shared fixtures and configuration
├── unit/                          # Unit tests (fast, isolated)
│   ├── __init__.py
│   ├── test_models.py            # Tests for Pydantic models
│   └── test_filesystem_adapter.py # Tests for FilesystemAdapter
├── integration/                   # Integration tests
│   ├── __init__.py
│   └── test_endpoints.py         # Tests for FastAPI endpoints
└── semantic/                      # Semantic integrity tests
    ├── __init__.py
    └── test_integrity.py         # Semantic consistency tests
```

## Prerequisites

### All Platforms

- **Python**: 3.11 or higher
- **pip**: Latest version recommended

### For Docker Testing

- **Docker**: Latest stable version
- **Docker Compose**: V2 or higher

### Verify Installation

```bash
# Check Python version
python3 --version  # or python --version on Windows

# Check pip
pip --version

# Check Docker (optional)
docker --version
docker-compose --version  # or docker compose version
```

## Quick Start

### Linux/macOS

```bash
# Clone and navigate to repository
cd /path/to/Semantic-Architecture

# Run all tests with coverage
./run-tests.sh coverage

# Or run specific test types
./run-tests.sh unit
./run-tests.sh integration
./run-tests.sh semantic
```

### Windows (PowerShell)

```powershell
# Navigate to repository
cd C:\path\to\Semantic-Architecture

# Run all tests
.\run-tests.ps1 all

# Or run specific test types
.\run-tests.ps1 unit
.\run-tests.ps1 integration
.\run-tests.ps1 coverage
```

### Docker (All Platforms)

```bash
# Build and run all tests
./run-tests-docker.sh all

# Run specific test types
./run-tests-docker.sh unit
./run-tests-docker.sh integration
```

## Running Tests Locally

### Step 1: Set Up Virtual Environment

#### Linux/macOS

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt
```

#### Windows (PowerShell)

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Note: If you get an execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements-dev.txt
```

### Step 2: Run Tests

#### Run All Tests

```bash
pytest -v
```

#### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit -v -m unit

# Integration tests only
pytest tests/integration -v -m integration

# Semantic tests only
pytest tests/semantic -v -m semantic
```

#### Run with Coverage

```bash
# Generate coverage report
pytest --cov=mcp_server --cov-report=term-missing --cov-report=html

# View HTML report (opens in browser)
# Linux/macOS
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

#### Run Specific Test File

```bash
pytest tests/unit/test_models.py -v
```

#### Run Specific Test Function

```bash
pytest tests/unit/test_models.py::TestSemanticNode::test_valid_semantic_node -v
```

### Step 3: Run with Different Options

```bash
# Stop at first failure
pytest -x

# Run in parallel (faster)
pytest -n auto

# Show local variables on failure
pytest --showlocals

# Run only failed tests from last run
pytest --lf

# Verbose output with full tracebacks
pytest -vv --tb=long
```

## Running Tests in Docker

### Build Test Containers

```bash
./run-tests-docker.sh build
```

### Run All Tests

```bash
./run-tests-docker.sh all
```

### Run Specific Test Types

```bash
# Unit tests in Docker
./run-tests-docker.sh unit

# Integration tests (with server)
./run-tests-docker.sh integration

# Run with coverage
./run-tests-docker.sh coverage
```

### Start MCP Server for Manual Testing

```bash
./run-tests-docker.sh server
```

The server will be available at `http://localhost:8000`. Access API documentation at `http://localhost:8000/docs`.

### Clean Up Docker Resources

```bash
./run-tests-docker.sh clean
```

## Platform-Specific Instructions

### Windows Detailed Setup

1. **Install Python**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify: `python --version`

2. **Install Git** (if not installed)
   - Download from [git-scm.com](https://git-scm.com/download/win)

3. **Set Execution Policy** (PowerShell)
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Create and Activate Virtual Environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

5. **Install Dependencies**
   ```powershell
   pip install -r requirements-dev.txt
   ```

6. **Run Tests**
   ```powershell
   .\run-tests.ps1 all
   ```

### macOS Detailed Setup

1. **Install Homebrew** (if not installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**
   ```bash
   brew install python@3.12
   ```

3. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Run Tests**
   ```bash
   ./run-tests.sh all
   ```

### Linux Detailed Setup

1. **Install Python** (if not already installed)
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv

   # Fedora/RHEL
   sudo dnf install python3 python3-pip

   # Arch
   sudo pacman -S python python-pip
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Run Tests**
   ```bash
   ./run-tests.sh all
   ```

## Test Categories

### Unit Tests (`tests/unit/`)

Fast, isolated tests that verify individual components without external dependencies.

**Markers**: `@pytest.mark.unit`

**What's tested**:
- Pydantic model validation and serialization
- FilesystemAdapter functionality
- Utility functions
- Security features (path traversal prevention, input sanitization)

**Run with**:
```bash
pytest tests/unit -v -m unit
```

### Integration Tests (`tests/integration/`)

Tests that verify the FastAPI application endpoints and service integration.

**Markers**: `@pytest.mark.integration`

**What's tested**:
- All HTTP endpoints (GET/POST)
- Request/response handling
- Error handling and status codes
- CORS configuration
- OpenAPI documentation

**Run with**:
```bash
pytest tests/integration -v -m integration
```

### Semantic Integrity Tests (`tests/semantic/`)

Tests that verify semantic consistency, data integrity, and cross-platform behavior.

**Markers**: `@pytest.mark.semantic`

**What's tested**:
- Semantic consistency across scopes
- Data validation rules
- Cross-environment compatibility
- Edge cases and boundary conditions
- Unicode and special character handling

**Run with**:
```bash
pytest tests/semantic -v -m semantic
```

## CI/CD Integration

### GitHub Actions Workflow

The repository includes a GitHub Actions workflow (`.github/workflows/test.yml`) that:

1. Runs tests on multiple platforms (Linux, macOS, Windows)
2. Tests with multiple Python versions (3.11, 3.12)
3. Builds and tests Docker images
4. Generates and uploads coverage reports
5. Creates test result artifacts

### Running Tests in CI

Tests run automatically on:
- Pull requests
- Pushes to main branch
- Manual workflow dispatch

### View Test Results

1. Go to the "Actions" tab in GitHub
2. Select the workflow run
3. View test results and coverage reports in artifacts

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'mcp_server'`

**Solution**:
```bash
# Ensure you're in the repository root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or reinstall in development mode
pip install -e .
```

#### 2. Permission Denied (Linux/macOS)

**Problem**: `Permission denied` when running scripts

**Solution**:
```bash
chmod +x run-tests.sh
chmod +x run-tests-docker.sh
```

#### 3. Virtual Environment Not Activating (Windows)

**Problem**: PowerShell execution policy prevents script execution

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 4. Docker Tests Failing

**Problem**: Docker containers not starting or tests timing out

**Solution**:
```bash
# Clean up Docker resources
docker-compose -f docker-compose.test.yml down -v
docker system prune -f

# Rebuild containers
./run-tests-docker.sh build
```

#### 5. Test Fixtures Not Found

**Problem**: `fixture 'xxx' not found`

**Solution**: Ensure `conftest.py` is in the tests directory and properly configured.

#### 6. Slow Tests

**Problem**: Tests taking too long

**Solution**:
```bash
# Run tests in parallel
pytest -n auto

# Run only fast tests
pytest -m "not slow"

# Skip integration tests
pytest -m "not integration"
```

### Getting Help

1. Check test output for detailed error messages
2. Review pytest documentation: https://docs.pytest.org/
3. Check the repository issues for known problems
4. Run tests with increased verbosity: `pytest -vv --tb=long`

## Test Development Guidelines

### Adding New Tests

1. **Choose the correct category**: unit, integration, or semantic
2. **Use appropriate markers**: `@pytest.mark.unit`, etc.
3. **Follow naming conventions**: `test_*.py` for files, `test_*` for functions
4. **Use fixtures** from `conftest.py` to avoid duplication
5. **Write clear test names** that describe what's being tested
6. **Add docstrings** to explain complex test logic

### Example Test

```python
import pytest
from mcp_server.models import SemanticNode

class TestSemanticNode:
    """Test SemanticNode model."""
    
    @pytest.mark.unit
    def test_valid_semantic_node(self):
        """Test creating a valid semantic node."""
        node = SemanticNode(
            id="test-node",
            scope="module",
            name="Test Module"
        )
        assert node.id == "test-node"
        assert node.scope == "module"
```

## Coverage Goals

- **Overall**: Target 80%+ code coverage
- **Unit Tests**: 90%+ coverage of core logic
- **Integration Tests**: 80%+ coverage of endpoints
- **Critical Paths**: 100% coverage of security-related code

## Performance Benchmarks

- **Unit Tests**: < 5 seconds total
- **Integration Tests**: < 30 seconds total
- **Full Suite**: < 60 seconds total
- **Docker Build**: < 2 minutes

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Docker Testing Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## License

This testing suite is part of the Semantic Architecture project and is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
