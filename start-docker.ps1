#Requires -Version 5.1

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

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

function Get-DockerInfo {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        throw 'Docker is not installed or not on PATH. Install Docker Desktop first.'
    }

    try {
        $info = & docker info --format '{{.OSType}}'
    } catch {
        throw 'Docker engine does not appear to be running. Start Docker Desktop and try again.'
    }

    $trimmed = ($info | ForEach-Object { $_.Trim() }) -join ''
    if (-not $trimmed) { $trimmed = 'unknown' }
    if ($trimmed -ne 'linux') {
        throw "Docker Desktop is not in Linux container mode (current OSType='$trimmed'). Switch to Linux containers and retry."
    }
}

function Initialize-Compose {
    $compose = $null
    $label = $null

    if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
        $compose = @{ Executable = 'docker-compose'; Args = @() }
        $label = 'docker-compose'
    } else {
        try {
            & docker compose version *> $null
            $compose = @{ Executable = 'docker'; Args = @('compose') }
            $label = 'docker compose'
        } catch {
            throw 'Docker Compose is not installed. Install docker-compose or enable Docker Compose v2.'
        }
    }

    return [pscustomobject]@{
        Command = $compose
        Label   = $label
    }
}

function Invoke-Compose {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    & $script:ComposeCommand.Executable @($script:ComposeCommand.Args + $Args)
    return $LASTEXITCODE
}

Push-Location $PSScriptRoot
try {
    Write-Host "`u{1F433} Starting Semantic Architecture MCP Server (Docker Mode)" -ForegroundColor Cyan
    Write-Host "=========================================================="

    Get-DockerInfo

    $dockerVersion = & docker --version
    $composeInfo = Initialize-Compose
    $script:ComposeCommand = $composeInfo.Command

    Write-Host "`u{2714} Docker: $dockerVersion" -ForegroundColor Green
    Write-Host "`u{2714} Docker Compose: $($composeInfo.Label)" -ForegroundColor Green

    switch ($Mode) {
        'dev' {
            Write-Host ''
            Write-Host 'Starting in DEVELOPMENT mode with hot-reload...'
            Write-Host '=========================================================='
            $exit = Invoke-Compose -Args @('up','--build','mcp-server-dev')
            if ($exit -ne 0) {
                throw "Docker Compose failed to start development service (exit code $exit)."
            }
        }
        'prod' {
            Write-Host ''
            Write-Host 'Starting in PRODUCTION mode with multiple workers...'
            Write-Host '=========================================================='
            $exit = Invoke-Compose -Args @('up','--build','-d','mcp-server-prod')
            if ($exit -ne 0) {
                throw "Docker Compose failed to start production service (exit code $exit)."
            }
            Write-Host ''
            Write-Host '✓ Server started in background'
            Write-Host '  - API:  http://localhost:8000'
            Write-Host '  - Docs: http://localhost:8000/docs'
            Write-Host ''
            Write-Host "View logs with: $($composeInfo.Label) logs -f mcp-server-prod"
            Write-Host "Stop server with: $($composeInfo.Label) down"
        }
        'stop' {
            Write-Host ''
            Write-Host 'Stopping all containers...'
            $exit = Invoke-Compose -Args @('down')
            if ($exit -ne 0) {
                throw "Docker Compose failed to stop containers (exit code $exit)."
            }
            Write-Host '✓ Containers stopped'
        }
    }
}
finally {
    Pop-Location
}
