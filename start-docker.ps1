#Requires -Version 5.1

<#
    PowerShell startup script for Docker deployment (Windows / pwsh)
    Parity with start-docker.sh

    Usage (pwsh):
      pwsh -File ./start-docker.ps1            # defaults to dev
      pwsh -File ./start-docker.ps1 -Mode dev  # dev with hot-reload
      pwsh -File ./start-docker.ps1 -Mode prod # prod in background
      pwsh -File ./start-docker.ps1 -Mode stop # stop containers
#>

param(
    [ValidateSet('dev','prod','stop')]
    [string]$Mode = 'dev'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Push-Location $PSScriptRoot
try {
    Write-Host "`u{1F433} Starting Semantic Architecture MCP Server (Docker Mode)" -ForegroundColor Cyan
    Write-Host "=========================================================="

    # Check if Docker is installed
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Error 'Docker is not installed or not on PATH. Please install Docker Desktop first.'
        exit 1
    }

    # Ensure Docker engine is running and in Linux container mode
    try {
        $osType = (& docker info --format '{{.OSType}}' 2>$null).Trim()
    } catch {
        Write-Error 'Docker engine does not appear to be running. Start Docker Desktop and try again.'
        exit 1
    }
    if (-not $osType) { $osType = 'unknown' }
    if ($osType -ne 'linux') {
        Write-Error "Docker Desktop is not in Linux container mode (current OSType='$osType'). Switch to Linux containers and retry."
        exit 1
    }

    # Determine Compose command (v1 docker-compose or v2 docker compose)
    $composeCmd = $null
    if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
        $composeCmd = 'docker-compose'
    } else {
        try {
            $null = & docker compose version 2>$null
            $composeCmd = 'docker compose'
        } catch {
            Write-Error 'Docker Compose is not installed. Install docker-compose or ensure Docker Compose v2 is available.'
            exit 1
        }
    }

    $dockerVersion = (& docker --version)
    Write-Host "`u{2714} Docker: $dockerVersion" -ForegroundColor Green
    Write-Host "`u{2714} Docker Compose: $composeCmd" -ForegroundColor Green

    switch ($Mode) {
        'dev' {
            Write-Host ''
            Write-Host 'Starting in DEVELOPMENT mode with hot-reload...'
            Write-Host '=========================================================='
            & $composeCmd up --build mcp-server-dev
            if ($LASTEXITCODE -ne 0) {
                throw "Docker Compose failed to start development service (exit code $LASTEXITCODE)."
            }
        }
        'prod' {
            Write-Host ''
            Write-Host 'Starting in PRODUCTION mode with multiple workers...'
            Write-Host '=========================================================='
            & $composeCmd up --build -d mcp-server-prod
            if ($LASTEXITCODE -ne 0) {
                throw "Docker Compose failed to start production service (exit code $LASTEXITCODE)."
            }
            Write-Host ''
            Write-Host '✓ Server started in background'
            Write-Host '  - API:  http://localhost:8000'
            Write-Host '  - Docs: http://localhost:8000/docs'
            Write-Host ''
            Write-Host "View logs with: $composeCmd logs -f mcp-server-prod"
            Write-Host "Stop server with: $composeCmd down"
        }
        'stop' {
            Write-Host ''
            Write-Host 'Stopping all containers...'
            & $composeCmd down
            if ($LASTEXITCODE -ne 0) {
                throw "Docker Compose failed to stop containers (exit code $LASTEXITCODE)."
            }
            Write-Host '✓ Containers stopped'
        }
    }
}
finally {
    Pop-Location
}
