# Start the Semantic Architecture MCP Server in Docker on Windows
# Usage: .\start-docker.ps1 [dev|prod|stop]

param(
    [ValidateSet("dev", "prod", "stop")]
    [string]$Mode = "dev"
)

Write-Host "🐳 Starting Semantic Architecture MCP Server (Docker Mode)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker command failed"
    }
    Write-Host "✓ Docker version: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed or not running" -ForegroundColor Red
    Write-Host "   Please install Docker Desktop from https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check Docker Compose (support both v1 and v2)
$composeCmd = $null
try {
    docker-compose --version > $null 2>&1
    if ($LASTEXITCODE -eq 0) {
        $composeCmd = "docker-compose"
    }
} catch {
    # docker-compose not found
}

if (-not $composeCmd) {
    try {
        docker compose version > $null 2>&1
        if ($LASTEXITCODE -eq 0) {
            $composeCmd = "docker compose"
        }
    } catch {
        # docker compose not found
    }
}

if (-not $composeCmd) {
    Write-Host "❌ Docker Compose is not installed" -ForegroundColor Red
    Write-Host "   Docker Desktop includes Compose. Please ensure Docker Desktop is properly installed." -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Docker Compose: $composeCmd" -ForegroundColor Green
Write-Host ""

# Build and start based on mode
switch ($Mode) {
    "dev" {
        Write-Host "Starting in DEVELOPMENT mode with hot-reload..." -ForegroundColor Yellow
        Write-Host "==========================================================" -ForegroundColor Cyan
        Write-Host ""
        
        if ($composeCmd -eq "docker-compose") {
            & docker-compose up --build mcp-server-dev
        } else {
            docker compose up --build mcp-server-dev
        }
    }
    
    "prod" {
        Write-Host "Starting in PRODUCTION mode with multiple workers..." -ForegroundColor Yellow
        Write-Host "==========================================================" -ForegroundColor Cyan
        Write-Host ""
        
        if ($composeCmd -eq "docker-compose") {
            & docker-compose up --build -d mcp-server-prod
        } else {
            docker compose up --build -d mcp-server-prod
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✓ Server started in background" -ForegroundColor Green
            Write-Host "  - API: http://localhost:8000" -ForegroundColor White
            Write-Host "  - Docs: http://localhost:8000/docs" -ForegroundColor White
            Write-Host ""
            Write-Host "View logs with: $composeCmd logs -f mcp-server-prod" -ForegroundColor Yellow
            Write-Host "Stop server with: .\start-docker.ps1 stop" -ForegroundColor Yellow
        } else {
            Write-Host "❌ Failed to start server" -ForegroundColor Red
            exit 1
        }
    }
    
    "stop" {
        Write-Host "Stopping all containers..." -ForegroundColor Yellow
        Write-Host ""
        
        if ($composeCmd -eq "docker-compose") {
            & docker-compose down
        } else {
            docker compose down
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Containers stopped" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Some containers may still be running" -ForegroundColor Yellow
        }
    }
}
