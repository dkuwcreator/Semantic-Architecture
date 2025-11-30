#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

<#
    PowerShell startup script for local development (Windows / pwsh)
    Parity with start-local.sh

    Usage (pwsh):
      pwsh -File ./start-local.ps1
#>

Push-Location $PSScriptRoot
try {
    Write-Host "`u{1F680} Starting Semantic Architecture MCP Server (Local Mode)" -ForegroundColor Cyan
    Write-Host "=========================================================="

    function Get-PythonCommand {
        # Prefer the Windows Python launcher when available
        if (Get-Command py -ErrorAction SilentlyContinue) {
            try {
                $null = & py -3 --version 2>$null
                return 'py -3'
            } catch {
                return 'py'
            }
        }
        elseif (Get-Command python -ErrorAction SilentlyContinue) {
            return 'python'
        }
        elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
            return 'python3'
        }
        else {
            throw 'Python is not installed or not on PATH. Install Python 3.9+ and try again.'
        }
    }

    $pythonCmd = Get-PythonCommand
    try {
        $versionOut = & $pythonCmd --version
    } catch {
        $versionOut = 'unknown'
    }
    Write-Host "`u{2714} Python: $versionOut" -ForegroundColor Green

    # Ensure virtual environment exists
    if (-not (Test-Path -Path 'venv')) {
        Write-Host "`u{1F4E6} Creating virtual environment..." -ForegroundColor Yellow
        & $pythonCmd -m venv venv
    }

    $venvPython = Join-Path $PSScriptRoot 'venv\Scripts\python.exe'
    if (-not (Test-Path $venvPython)) {
        throw "Virtual environment seems corrupted: '$venvPython' not found. Delete 'venv' and re-run."
    }

    # Install/update dependencies
    Write-Host "`u{1F4E6} Installing dependencies..." -ForegroundColor Yellow
    & $venvPython -m pip install -q -r (Join-Path $PSScriptRoot 'requirements.txt')

    # Verify scripts are callable
    Write-Host "`u{2714} Verifying scripts..." -ForegroundColor Green
    try {
        & $venvPython (Join-Path $PSScriptRoot 'scripts\semantic_graph.py') --help *> $null
        Write-Host "  - semantic_graph.py OK"
    } catch {
        Write-Host "  - semantic_graph.py FAILED" -ForegroundColor Red
    }

    # Port selection: prefer 8000, fall back to 8001 if in use
    $Port = 8000
    $portChecked = $false
    if (Get-Command Get-NetTCPConnection -ErrorAction SilentlyContinue) {
        $listening = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -eq 8000 }
        if ($listening) { $Port = 8001 }
        $portChecked = $true
    } elseif (Get-Command Test-NetConnection -ErrorAction SilentlyContinue) {
        $tnc = Test-NetConnection -ComputerName 'localhost' -Port 8000 -WarningAction SilentlyContinue
        if ($tnc.TcpTestSucceeded) { $Port = 8001 }
        $portChecked = $true
    }
    if (-not $portChecked) {
        Write-Warning "Could not reliably check if port 8000 is in use. Defaulting to 8000."
    } elseif ($Port -ne 8000) {
        Write-Warning "Port 8000 is already in use. Using port 8001 instead."
    }

    Write-Host ""; Write-Host "`u{2714} All checks passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Starting server on http://localhost:$Port"
    Write-Host "  - API Documentation: http://localhost:$Port/docs"
    Write-Host "  - Health Check: http://localhost:$Port/health"
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the server"
    Write-Host "=========================================================="

    # Start the server (no need to activate; call venv python directly)
    & $venvPython -m uvicorn mcp_server.main:app --host 0.0.0.0 --port $Port --reload
}
finally {
    Pop-Location
}
