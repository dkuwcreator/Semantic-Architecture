# Run tests on Windows with PowerShell
# Usage: .\run-tests.ps1 [unit|integration|semantic|coverage|quick|all]

param(
    [string]$TestType = "all"
)

Write-Host "=== Semantic Architecture MCP Server - Test Runner ===" -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Using $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements-dev.txt

# Run tests based on argument
switch ($TestType) {
    "unit" {
        Write-Host "Running unit tests..." -ForegroundColor Green
        pytest tests/unit -v --tb=short -m unit
    }
    "integration" {
        Write-Host "Running integration tests..." -ForegroundColor Green
        pytest tests/integration -v --tb=short -m integration
    }
    "semantic" {
        Write-Host "Running semantic integrity tests..." -ForegroundColor Green
        pytest tests/semantic -v --tb=short -m semantic
    }
    "coverage" {
        Write-Host "Running all tests with coverage..." -ForegroundColor Green
        pytest -v --tb=short --cov=mcp_server --cov-report=term-missing --cov-report=html
        Write-Host "Coverage report generated in htmlcov\index.html" -ForegroundColor Green
    }
    "quick" {
        Write-Host "Running quick tests (unit only)..." -ForegroundColor Green
        pytest tests/unit -v --tb=short -x
    }
    "all" {
        Write-Host "Running all tests..." -ForegroundColor Green
        pytest -v --tb=short
    }
    default {
        Write-Host "Unknown test type: $TestType" -ForegroundColor Red
        Write-Host "Usage: .\run-tests.ps1 [unit|integration|semantic|coverage|quick|all]"
        exit 1
    }
}

# Check exit code
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Tests passed!" -ForegroundColor Green
} else {
    Write-Host "✗ Tests failed!" -ForegroundColor Red
    exit 1
}
