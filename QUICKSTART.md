# Quick Start: Semantic Architecture (Non-Server)

This repository is documentation-first and includes supporting scripts for semantic validation and reporting.

## Prerequisites

- Python (see [pytest.ini](pytest.ini) for the repo’s baseline)

## Local Setup

Create a virtual environment and install dependencies:

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run a Non-Server Workflow

Run the semantic validator script and request JSON output:

```bash
python scripts/semantic_validator.py --help
python scripts/semantic_validator.py --targets . --outputFormat json
```

## Testing

- Windows: `./run-tests.ps1 all`
- Linux/macOS: `./run-tests.sh all`
