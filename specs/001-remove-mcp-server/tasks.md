---

description: "Task list for implementing 001-remove-mcp-server"
---

# Tasks: Remove MCP Server & Repo Cleanup

**Input**: Design documents from `specs/001-remove-mcp-server/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish a clear, shared understanding of scope and validation

- [x] T001 Review scope and acceptance criteria in specs/001-remove-mcp-server/spec.md
- [x] T002 [P] Create/update an inventory of MCP-server-related artifacts to change in specs/001-remove-mcp-server/research.md
- [x] T003 [P] Confirm/extend verification steps for this feature in specs/001-remove-mcp-server/quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Identify all MCP touchpoints so removal is complete and coherent

**⚠️ CRITICAL**: No user story work should begin until this phase is complete

- [x] T004 [P] Locate and record all `mcp_server` references (docs/scripts/tests/config) in specs/001-remove-mcp-server/research.md
- [x] T005 [P] Locate and record FastAPI/Uvicorn/httpx/TestClient references in specs/001-remove-mcp-server/research.md
- [x] T006 [P] Record the post-removal coverage target decision (e.g., `scripts/`) in specs/001-remove-mcp-server/plan.md
- [x] T007 [P] Identify server-only tests to rewrite/retire and record a mapping plan in specs/001-remove-mcp-server/research.md
- [x] T008 Verify generated-artifact ignore coverage (htmlcov/, coverage.xml) in .gitignore

**Checkpoint**: Foundation ready — implementation tasks can begin

---

## Phase 3: User Story 1 — Use Repository Without MCP Server (Priority: P1) 🎯 MVP

**Goal**: Repository no longer ships or presents an MCP server deliverable.

**Independent Test**: A maintainer can review repo contents + top-level docs and see no instructions to run/deploy an MCP server and no MCP server deliverable.

### Implementation

- [x] T009 [US1] Remove the MCP server package directory in mcp_server/
- [x] T010 [P] [US1] Remove MCP server positioning/links in README.md
- [x] T011 [P] [US1] Replace MCP-server quickstart content with non-server guidance in QUICKSTART.md
- [x] T012 [P] [US1] Remove MCP-server deployment/start instructions in DEPLOYMENT.md
- [x] T013 [P] [US1] Remove server startup script (PowerShell) in start-local.ps1
- [x] T014 [P] [US1] Remove server startup script (shell) in start-local.sh
- [x] T015 [P] [US1] Remove server docker startup script (PowerShell) in start-docker.ps1
- [x] T016 [P] [US1] Remove server docker startup script (shell) in start-docker.sh
- [x] T017 [P] [US1] Remove MCP server container entrypoint/build instructions in Dockerfile
- [x] T018 [P] [US1] Remove MCP server docker runtime wiring in docker-compose.yml

**Checkpoint**: MCP server is no longer a shipped/positioned deliverable.

---

## Phase 4: User Story 2 — Keep Core Tooling Usable (Priority: P2)

**Goal**: Non-server scripts and the automated test workflow still run successfully after removal.

**Independent Test**: Run the standard test workflow and at least one non-server semantic workflow without MCP server dependencies.

### Implementation

- [x] T019 [US2] Remove server runtime dependencies from requirements.txt
- [x] T020 [P] [US2] Remove unused server-test dependencies from requirements-dev.txt
- [x] T021 [US2] Update pytest configuration and coverage target away from `mcp_server` in pytest.ini
- [x] T022 [P] [US2] Update Windows test runner to match new layout in run-tests.ps1
- [x] T023 [P] [US2] Update shell test runner to match new layout in run-tests.sh
- [x] T024 [P] [US2] Update Docker-based test runner to match new layout in run-tests-docker.sh
- [x] T025 [P] [US2] Update Docker test compose to remove `mcp_server` mounts/env and fix pytest args in docker-compose.test.yml
- [x] T026 [US2] Rewrite shared fixtures to remove FastAPI clients and `mcp_server` imports in tests/conftest.py
- [x] T027 [P] [US2] Convert integration tests from HTTP endpoints to script-based checks in tests/integration/test_endpoints.py
- [x] T028 [P] [US2] Replace Pydantic model tests with JSON schema/output tests for scripts in tests/unit/test_models.py
- [x] T029 [P] [US2] Create a small helper to run scripts and parse JSON output in tests/helpers/script_runner.py
- [x] T030 [US2] Replace FilesystemAdapter tests with script-runner tests in tests/unit/test_filesystem_adapter.py

**Checkpoint**: `run-tests.*` succeeds without MCP server dependencies.

---

## Phase 5: User Story 3 — Reduce Confusion for New Readers (Priority: P3)

**Goal**: README and docs provide a coherent non-server “start here” path.

**Independent Test**: A new reader can follow README → docs/QUICKSTART to run a non-server semantic script without encountering server setup.

### Implementation

- [x] T031 [P] [US3] Remove remaining MCP server references in docs/ (edit any files discovered by search)
- [x] T032 [P] [US3] Remove remaining MCP server references in examples/ (edit any files discovered by search)
- [x] T033 [US3] Ensure QUICKSTART.md includes at least one concrete non-server workflow using scripts/semantic_validator.py

**Checkpoint**: Onboarding path is coherent and non-server.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup and verification against success criteria

- [x] T034 [P] Remove committed generated coverage artifacts in htmlcov/ and coverage.xml
- [x] T035 [P] Remove any committed test artifact directory in test-results/
- [x] T036 Create a validation report with grep/test evidence in specs/001-remove-mcp-server/validation-report.md
- [x] T037 [P] Regenerate Copilot agent context after implementation in .github/agents/copilot-instructions.md

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1) → Foundational (Phase 2) → User Stories (Phases 3–5) → Polish (Phase 6)

### User Story Dependencies

- **US1 (P1)**: Depends on Foundational; unblocks removal of server assets.
- **US2 (P2)**: Depends on US1 changes to remove server; updates dependencies/tests to remain green.
- **US3 (P3)**: Depends on US1 doc changes; final consistency pass across docs/examples.

### Parallel Opportunities (examples)

- US1: T010–T018 can run in parallel across separate files.
- US2: T020, T022–T025, T027–T029 can run in parallel across separate files.
- US3: T031 and T032 can run in parallel.

---

## Parallel Example: User Story 1

- Run in parallel:
  - T010 (README.md)
  - T011 (QUICKSTART.md)
  - T012 (DEPLOYMENT.md)
  - T013–T016 (start scripts)
  - T017 (Dockerfile)
  - T018 (docker-compose.yml)

## Parallel Example: User Story 2

- Run in parallel:
  - T020 (requirements-dev.txt)
  - T022 (run-tests.ps1)
  - T023 (run-tests.sh)
  - T025 (docker-compose.test.yml)
  - T029 (tests/helpers/script_runner.py)

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1–2
2. Complete Phase 3 (US1)
3. Validate SC-001 and SC-004 via repo-wide search and doc review

### Incremental Delivery

1. US1: Remove MCP deliverable + remove server docs/scripts
2. US2: Make tests and non-server workflows pass without server deps
3. US3: Final consistency pass for onboarding
4. Polish: Remove generated artifacts and capture validation evidence
