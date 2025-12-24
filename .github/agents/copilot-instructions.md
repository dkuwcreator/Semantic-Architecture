# Semantic-Architecture Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-24

## Active Technologies

- Python >= 3.11 (per `pytest.ini`) (001-remove-mcp-server)
- pytest + coverage (pytest-cov/coverage) for automated validation

## Project Structure

```text
adapters/
data/
docs/
examples/
scripts/
specs/
templates/
tests/
```

## Commands

- Local non-server workflow: `python scripts/semantic_validator.py --targets . --outputFormat json`
- Run tests (Windows): `./run-tests.ps1 all`
- Run tests (Linux/macOS): `./run-tests.sh all`
- Run pytest directly: `pytest`

## Code Style

Python >= 3.11 (per `pytest.ini`): Follow standard conventions

## Recent Changes

- 001-remove-mcp-server: Removed MCP server runtime; repo is documentation + non-server scripts

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
