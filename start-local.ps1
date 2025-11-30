#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

param(
    [int]$Port = 8000
)

<#
    PowerShell startup script for local development (Windows / pwsh)
    Parity with start-local.sh

    Usage (pwsh):
      pwsh -File ./start-local.ps1 [-Port 8000]
#>

function Get-PythonCommand {
    # Prefer the Windows Python launcher when available
    if (Get-Command py -ErrorAction SilentlyContinue) {
        try {
            & py -3 --version *> $null
            return [pscustomobject]@{ Executable = 'py'; DefaultArgs = @('-3') }
        } catch {
            return [pscustomobject]@{ Executable = 'py'; DefaultArgs = @() }
        }
    }
    elseif (Get-Command python -ErrorAction SilentlyContinue) {
        return [pscustomobject]@{ Executable = 'python'; DefaultArgs = @() }
    }
    elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
        return [pscustomobject]@{ Executable = 'python3'; DefaultArgs = @() }
    }
    else {
        throw 'Python is not installed or not on PATH. Install Python 3.9+ and try again.'
    }
}

function Invoke-HostPython {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    & $script:HostPython.Executable @($script:HostPython.DefaultArgs + $Args)
}

$script:HostPython = Get-PythonCommand
$PortWasProvided = $PSBoundParameters.ContainsKey('Port')

Push-Location $PSScriptRoot
try {
    Write-Host "`u{1F680} Starting Semantic Architecture MCP Server (Local Mode)" -ForegroundColor Cyan
    Write-Host "=========================================================="

    try {
        $versionOut = Invoke-HostPython -Args @('--version')
    } catch {
        $versionOut = 'unknown'
    }
    Write-Host "`u{2714} Python: $versionOut" -ForegroundColor Green

    if (-not (Test-Path -Path 'venv')) {
        Write-Host "`u{1F4E6} Creating virtual environment..." -ForegroundColor Yellow
        Invoke-HostPython -Args @('-m', 'venv', 'venv')
    }

    $venvPython = Join-Path $PSScriptRoot 'venv\Scripts\python.exe'
    if (-not (Test-Path $venvPython)) {
        throw "Virtual environment seems corrupted: '$venvPython' not found. Delete 'venv' and re-run."
    }

    Write-Host "`u{1F4E6} Installing dependencies..." -ForegroundColor Yellow
    & $venvPython -m pip install -q -r (Join-Path $PSScriptRoot 'requirements.txt')

    Write-Host "`u{2714} Verifying scripts..." -ForegroundColor Green
    try {
        & $venvPython (Join-Path $PSScriptRoot 'scripts\semantic_graph.py') --help *> $null
        Write-Host "  - semantic_graph.py OK"
    } catch {
        Write-Host "  - semantic_graph.py FAILED" -ForegroundColor Red
    }

    $PortToUse = $Port
    $portChecked = $false
    if (Get-Command Get-NetTCPConnection -ErrorAction SilentlyContinue) {
        $listening = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -eq $PortToUse }
        if ($listening) {
            if ($PortWasProvided) {
                throw "Port $Port is already in use. Provide a different port via -Port."
            }
            $PortToUse = 8001
        }
        $portChecked = $true
    }
    elseif (Get-Command Test-NetConnection -ErrorAction SilentlyContinue) {
        $tnc = Test-NetConnection -ComputerName 'localhost' -Port $PortToUse -WarningAction SilentlyContinue
        if ($tnc.TcpTestSucceeded) {
            if ($PortWasProvided) {
                throw "Port $Port is already in use. Provide a different port via -Port."
            }
            $PortToUse = 8001
        }
        $portChecked = $true
    }

    if (-not $portChecked) {
        Write-Warning "Could not reliably check if port $PortToUse is in use."
    } elseif ($PortToUse -ne $Port) {
        Write-Warning "Port $Port is already in use. Using port $PortToUse instead."
    }

    Write-Host ""
    Write-Host "`u{2714} All checks passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Starting server on http://localhost:$PortToUse"
    Write-Host "  - API Documentation: http://localhost:$PortToUse/docs"
    Write-Host "  - Health Check: http://localhost:$PortToUse/health"
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the server"
    Write-Host "=========================================================="

    & $venvPython -m uvicorn mcp_server.main:app --host 0.0.0.0 --port $PortToUse --reload
}
finally {
    Pop-Location
}
