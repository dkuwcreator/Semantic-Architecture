# Phase 0 Research: Remove MCP Server & Repo Cleanup

**Feature**: [spec.md](spec.md)
**Date**: 2025-12-24

This feature is primarily a repository-scope removal and cleanup. Research here captures scoped decisions and how they will be validated.

## Decisions

### Decision: Remove MCP server deliverable
- **Rationale**: User request is to stop shipping/positioning this repo as an MCP server.
- **Alternatives considered**:
  - Keep server code but mark “deprecated”: rejected because it still ships/encourages server usage.
  - Keep server code behind a feature flag: rejected because it remains a deliverable and adds complexity.

### Decision: Keep repo purpose as “Semantic Architecture documentation + supporting tooling”
- **Rationale**: README already positions the repo as documentation-first; removal should reinforce that.
- **Alternatives considered**:
  - Replace with another server/runtime: rejected (explicit non-goal).

### Decision: Remove MCP-specific operational tooling
- **Rationale**: Start scripts, Docker compose, and deployment docs that exist solely to run the MCP server become misleading once the server is removed.
- **Alternatives considered**:
  - Keep docker/start scripts as generic Python tooling: rejected unless they provide value without server.

### Decision: Update tests/coverage configuration to match new package layout
- **Rationale**: Current pytest config targets `mcp_server` for coverage; once removed, tests must still run.
- **Alternatives considered**:
  - Keep coverage pointing at a non-existent package: rejected.

## Validation Approach (Research Outcome)

- Validate documentation entry points (README/QUICKSTART/DEPLOYMENT) no longer instruct “run/deploy MCP server”.
- Validate repository contents no longer include an MCP server deliverable.
- Validate `pytest`/existing test runner scripts run without MCP server dependencies.

## Inventory (Concrete Touchpoints)

This section enumerates known MCP server touchpoints discovered via repository search. It is used to ensure removal is complete.

### MCP server deliverable

- `mcp_server/` (package + routes/models/adapters)

### Primary documentation

- `QUICKSTART.md` (currently "Quick Start: MCP Server", endpoints, uvicorn troubleshooting)
- `DEPLOYMENT.md` (uvicorn commands, config references, docker mount examples)
- `README.md` (links/positioning for MCP server)
- `mcp_server/README.md` (server-specific documentation)

### Operational scripts

- `start-local.ps1`, `start-local.sh` (uvicorn startup)
- `start-docker.ps1`, `start-docker.sh` (compose-based server startup)

### Docker assets

- `Dockerfile` (uvicorn CMD pointing to `mcp_server.main:app`)
- `docker-compose.yml` (mounts `./mcp_server`)
- `docker-compose.test.yml` (mounts `./mcp_server`, sets `MCP_SERVER_URL`, and runs coverage for `mcp_server`)

### Test runner scripts

- `run-tests.ps1`, `run-tests.sh`, `run-tests-docker.sh` (all run pytest with `--cov=mcp_server`)

### Test documentation

- `tests/README.md` (positions integration tests as FastAPI endpoint tests; includes `--cov=mcp_server` examples)

### Ignore/config references

- `.dockerignore` (currently keeps `mcp_server/README.md` while excluding other markdown)
- `.local/.github-old/workflows/test.yml` (historical CI config includes `--cov=mcp_server`)

### Python deps and test configuration

- `requirements.txt` (FastAPI/Uvicorn/Pydantic-settings/python-multipart)
- `requirements-dev.txt` (includes `httpx` explicitly for FastAPI testing)
- `pytest.ini` (`--cov=mcp_server` and coverage `source = mcp_server`)

### Tests (server-coupled)

- `tests/conftest.py` (imports FastAPI `TestClient`, `httpx.AsyncClient`, `mcp_server.main`, `mcp_server.adapters`)
- `tests/integration/test_endpoints.py` (FastAPI endpoint integration tests)
- `tests/unit/test_models.py` (Pydantic model tests from `mcp_server.models`)
- `tests/unit/test_filesystem_adapter.py` (imports `mcp_server.adapters.FilesystemAdapter`)
- `tests/semantic/test_integrity.py` (imports `mcp_server` models/adapters in some tests)

### Generated artifacts (should not be committed post-cleanup)

- `htmlcov/`
- `coverage.xml`

## Mapping Plan (What Changes Where)

- Remove MCP deliverable: delete `mcp_server/`.
- Replace server tests: rewrite tests to validate non-server scripts under `scripts/` (JSON output + exit codes), and remove endpoint-centric integration testing.
- Remove server dependencies: drop FastAPI/Uvicorn/Pydantic-settings/python-multipart and any dev-only server-testing deps that become unused.
- Update coverage target: stop targeting `mcp_server` for coverage; target non-server code (planned: `scripts/`) or remove coverage options if no longer meaningful.
- Update docs: convert `QUICKSTART.md` and `DEPLOYMENT.md` to non-server guidance; remove all server endpoint lists.
- Update docker and start scripts: remove any Docker/compose/start assets that exist solely to run the server.

## Out of Scope

- Introducing any new server/runtime.
- Broad refactors unrelated to removing MCP server positioning/deliverable.
