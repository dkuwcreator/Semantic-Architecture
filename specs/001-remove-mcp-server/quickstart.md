# Quickstart: Remove MCP Server & Repo Cleanup (Planning)

**Feature**: [spec.md](spec.md)
**Date**: 2025-12-24

This quickstart describes how to validate the change once implemented.

## Validate Documentation Entry Points

- Confirm top-level docs do not instruct running or deploying an MCP server.
  - README: should describe the repo as documentation-first and tooling/validation scripts, not a server.
  - Root quickstart/deployment docs: should no longer describe server endpoints or uvicorn startup.

Suggested checks:

- Search for MCP server strings:
  - `mcp_server`
  - `uvicorn`
  - `FastAPI`
  - `http://localhost:8000/docs`

## Validate Repository Contents

- Confirm the repository no longer contains an MCP server deliverable (server package + server-only configuration).

Suggested checks:

- Ensure `mcp_server/` does not exist.

## Validate Tests

- Run the existing test workflow for the repository.
- Confirm tests do not require FastAPI/uvicorn/httpx unless still used by non-server tooling.

Suggested commands:

- Windows: `./run-tests.ps1 all`
- Linux/macOS: `./run-tests.sh all`
- Optional (coverage): `./run-tests.ps1 coverage` / `./run-tests.sh coverage` (after coverage target is updated)

## Validate Non-Server Workflow

- Run at least one non-server script and confirm it produces valid JSON output.
  - Example: `python scripts/semantic_validator.py --targets . --outputFormat json`

## Expected Outcome

- Repo is coherent as “Semantic Architecture docs + supporting tools”, without a server runtime.
