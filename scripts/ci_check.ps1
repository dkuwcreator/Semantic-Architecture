Param(
  [string]$Mode = "validate-all"
)

$ErrorActionPreference = 'Stop'

# Run validator (CI ruleset) and drift scanner; emit compact JSON result
$python = "python"

$validator = & $python "scripts/semantic_validator.py" --ruleset ci --targets . --outputFormat json 2>$null
$validatorObj = $null
try { $validatorObj = $validator | ConvertFrom-Json } catch { $validatorObj = @{ diagnostics=@(); summary=@{ errors=1; warnings=0 } } }

$base = if ($env:GITHUB_BASE_REF) { "origin/$($env:GITHUB_BASE_REF)" } else { "origin/main" }
$drift = & $python "scripts/semantic_drift_scanner.py" --baseRef $base --headRef HEAD 2>$null
$driftObj = $null
try { $driftObj = $drift | ConvertFrom-Json } catch { $driftObj = @{ drifts=@(); summary=@{ count=0 } } }

$errors = [int]$validatorObj.summary.errors
$warnings = [int]$validatorObj.summary.warnings

$result = if ($errors -gt 0) { "fail" } else { "pass" }

$out = @{ result=$result; counts=@{ errors=$errors; warnings=$warnings } } | ConvertTo-Json -Depth 6
Write-Output $out

if ($result -eq 'fail') { exit 1 } else { exit 0 }
