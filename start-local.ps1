# Start the Semantic Architecture MCP Server locally on Windows
# Usage: .\start-local.ps1

param(
    [int]$Port = 8000
)

Write-Host "🚀 Starting Semantic Architecture MCP Server (Local Mode)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "   Please install Python 3.11+ from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install/update dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
python -m pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Verify scripts are executable
Write-Host "✓ Verifying scripts..." -ForegroundColor Green
try {
    python scripts/semantic_graph.py --help > $null 2>&1
    Write-Host "  - semantic_graph.py OK" -ForegroundColor Green
} catch {
    Write-Host "  - semantic_graph.py FAILED" -ForegroundColor Red
}

# Check if port is available
$portInUse = $false
try {
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue -InformationLevel Quiet
    if ($connection) {
        $portInUse = $true
    }
} catch {
    # Port check failed, assume port is available
    $portInUse = $false
}

if ($portInUse) {
    Write-Host "⚠️  Port $Port is already in use. Using port 8001 instead." -ForegroundColor Yellow
    $Port = 8001
}

Write-Host ""
Write-Host "✓ All checks passed!" -ForegroundColor Green
Write-Host ""
Write-Host "Starting server on http://localhost:$Port" -ForegroundColor Cyan
Write-Host "  - API Documentation: http://localhost:$Port/docs" -ForegroundColor White
Write-Host "  - Health Check: http://localhost:$Port/health" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# Start the server
try {
    uvicorn mcp_server.main:app --host 0.0.0.0 --port $Port --reload
} catch {
    Write-Host ""
    Write-Host "❌ Server stopped with error: $_" -ForegroundColor Red
    exit 1
}
