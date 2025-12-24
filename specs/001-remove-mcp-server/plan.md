# Implementation Plan: Remove MCP Server & Repo Cleanup

**Branch**: `001-remove-mcp-server` | **Date**: 2025-12-24 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from [spec.md](spec.md)

## Summary

Remove the MCP server deliverable and MCP server-specific operational artifacts (dependencies, startup/deploy scripts, and documentation) while keeping the repository’s documentation-first purpose and ensuring existing non-server tooling and tests remain usable.

## Technical Context

**Language/Version**: Python >= 3.11 (per `pytest.ini`)  
**Primary Dependencies**: Runtime: Python standard library only (scripts under `scripts/`)  
**Storage**: N/A  
**Testing**: pytest (+ pytest-cov, pytest-xdist); coverage targets `scripts/` and tests execute scripts in-process where practical  
**Target Platform**: Cross-platform (PowerShell + shell scripts exist); Docker files present  
**Project Type**: Documentation-first repository with supporting Python tooling (non-server)  
**Performance Goals**: N/A  
**Constraints**: Avoid broad refactors; remove MCP-related deliverables and references; keep tests working  
**Scale/Scope**: Project-level cleanup across docs/scripts/tests/dependencies

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Minimum gates (from `.specify/memory/constitution.md`):

- Tool-agnostic purity: PASS. Removing an MCP server reduces tool/vendor coupling; tool-specific guidance remains isolated under `adapters/`.
- Bounded context: PASS. This is necessarily project-scoped because MCP server concerns currently span docs, scripts, dependencies, and tests.
- Meaning-first parity: PASS. Plan explicitly includes updating docs/instructions alongside behavior changes.
- Drift policy: PASS. No open ambiguities; if conflicts appear during implementation, record analysis in `tasks.md` before changes.
- Review integrity: PASS. This plan follows spec → plan → tasks → implement.

## Phase 0: Outline & Research

**Output**: [research.md](research.md)

All known decisions and validation approach are recorded in [research.md](research.md). No unresolved clarifications remain.

## Phase 1: Design & Contracts

**Prerequisite**: [research.md](research.md)

### Data Model

**Output**: [data-model.md](data-model.md)

No new entities or persistence are introduced by this feature.

### Contracts

**Output**: [contracts/README.md](contracts/README.md)

This feature does not add or change an external API contract.

### Quickstart (Validation)

**Output**: [quickstart.md](quickstart.md)

Defines validation steps once implementation is complete.

### Constitution Re-check (post-design)

- Tool-agnostic purity: PASS
- Bounded context: PASS
- Meaning-first parity: PASS
- Drift management: PASS

## Project Structure

### Documentation (this feature)

```text
specs/001-remove-mcp-server/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── README.md
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)
```text
adapters/
data/
docs/
examples/
scripts/
templates/
tests/

DEPLOYMENT.md
QUICKSTART.md
Dockerfile
docker-compose.test.yml
requirements.txt
requirements-dev.txt
pytest.ini
run-tests.*
```

**Structure Decision**: Maintain the existing documentation-first repository structure; remove the `mcp_server/` deliverable and any MCP server-only operational files/references. Do not introduce a replacement runtime.

## Complexity Tracking

No constitution violations anticipated.

## Phase 2: Planning (Task Outline)

This phase produces `tasks.md` via `/speckit.tasks`. The outline below defines task groups and expected validation.

### Task Group A — Remove MCP Server Code

- Remove `mcp_server/` and any server-only entrypoints.
- Remove/adjust imports and references to `mcp_server` in remaining code.

### Task Group B — Remove MCP Server Dependencies

- Remove FastAPI/Uvicorn/Pydantic server dependencies from `requirements.txt` if not used by remaining tooling.
- Remove dev-only server testing dependencies (e.g., `httpx`) from `requirements-dev.txt` if no longer used.

### Task Group C — Update Tests & Coverage

- Update `pytest.ini` coverage configuration to no longer target `mcp_server`.
- Update any tests that exist solely for the server; preserve semantic/tooling tests.
- Ensure `run-tests.*` scripts remain correct.

### Task Group D — Docs Cleanup

- Update root documentation (notably `QUICKSTART.md` and `DEPLOYMENT.md`) to remove MCP server start/deploy guidance and endpoint lists.
- Ensure README entry points do not imply a server runtime.

### Task Group E — Operational Scripts & Docker Assets

- Remove or rewrite `start-local.*` / `start-docker.*` / docker-compose assets if they exist only to run the MCP server.
- Keep only assets that support non-server workflows.

### Validation (must satisfy spec success criteria)

- **SC-001**: No MCP server positioning/instructions in primary docs, except explicit “not provided”.
- **SC-002**: Existing automated test workflow passes on clean checkout.
- **SC-003**: README → docs path enables at least one non-server semantic workflow.
- **SC-004**: No MCP server start/deploy instructions in operational docs.
