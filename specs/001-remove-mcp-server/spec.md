# Feature Specification: Remove MCP Server & Repo Cleanup

**Feature Branch**: `001-remove-mcp-server`  
**Created**: 2025-12-24  
**Status**: Draft  
**Input**: User description: "the current repo is setup as mcp server, this is not needed for now. I want it removed and the repo cleaned up."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Use Repository Without MCP Server (Priority: P1)

As a maintainer, I want the repository to no longer present itself as an MCP server so that the primary purpose (semantic architecture artifacts + supporting tooling) is clear and not coupled to a server runtime.

**Why this priority**: This is the core request and unblocks all other cleanup work.

**Independent Test**: Can be validated by reviewing repository contents and primary documentation to confirm there is no MCP server deliverable and no MCP server instructions.

**Acceptance Scenarios**:

1. **Given** the repository at the feature branch, **When** a maintainer reviews top-level project documentation, **Then** it does not instruct users to run or deploy an MCP server.
2. **Given** the repository at the feature branch, **When** a maintainer inspects repository contents, **Then** MCP server-specific code/configuration artifacts are removed or clearly separated such that the repo no longer provides an MCP server deliverable.
3. **Given** the repository at the feature branch, **When** a maintainer reads the README and quickstart guidance, **Then** it clearly states that MCP server support is not provided.
4. **Given** the repository at the feature branch, **When** a maintainer reviews operational/deployment guidance, **Then** MCP server-specific start/deploy instructions are not present.

---

### User Story 2 - Keep Core Tooling Usable (Priority: P2)

As a contributor, I want existing non-server workflows (tests, documentation reading, and local tooling scripts that support semantic architecture artifacts) to remain usable after MCP server removal.

**Why this priority**: Removing the server should not break the main value of the repo or force contributors to reverse-engineer how to use it.

**Independent Test**: Can be validated by running the existing automated tests and confirming documented non-server workflows still work.

**Acceptance Scenarios**:

1. **Given** a fresh clone on the feature branch, **When** a contributor runs the repository’s standard test workflow, **Then** the test workflow completes successfully without requiring an MCP server.
2. **Given** the repository’s existing non-server scripts and docs, **When** a contributor follows the documented steps, **Then** they can perform semantic validation/reporting tasks without encountering MCP server-related steps.
3. **Given** any remaining scripts and documentation, **When** a contributor follows them end-to-end, **Then** they are not blocked by missing MCP server components.

---

### User Story 3 - Reduce Confusion for New Readers (Priority: P3)

As a new reader, I want the repository entry points to be unambiguous so I can quickly understand what the repo is for and how to use it (without being routed into server deployment guidance).

**Why this priority**: Improves onboarding and reduces misalignment, but depends on the core removal work.

**Independent Test**: Can be validated by checking that primary docs consistently describe the repo purpose and do not include conflicting MCP server positioning.

**Acceptance Scenarios**:

1. **Given** a new reader starting from the README, **When** they follow the recommended “getting started” path, **Then** they encounter a coherent, non-server set of instructions and links.

---

### Edge Cases

- Existing users may rely on MCP server behavior; removal must be clearly communicated in docs to avoid confusion.
- Some scripts/configuration may reference server components indirectly; cleanup must remove or update those references.
- References may exist in multiple locations (documentation, examples, deployment files, CI/test scripts); cleanup must be comprehensive.
- If any server-related artifacts are required for future use, they must be explicitly out of scope for now or moved aside in a way that does not imply active support.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Repository MUST no longer be positioned as, or ship as, an MCP server deliverable.
- **FR-002**: Repository MUST remove MCP server-specific source, configuration, and documentation artifacts such that a user cannot reasonably interpret the repo as requiring an MCP server.
- **FR-003**: Repository MUST update or remove scripts and deployment/configuration materials that exist solely to run or deploy the MCP server.
- **FR-004**: Repository MUST keep existing non-server semantic architecture workflows usable (documentation consumption, semantic artifact generation/validation/reporting where currently supported).
- **FR-005**: Repository MUST ensure automated tests (as currently defined in the repo) run successfully without requiring an MCP server.
- **FR-006**: Repository MUST remove or update documentation links that reference MCP server setup so that top-level docs provide a consistent “getting started” path.
- **FR-007**: Repository MUST include a clear scope statement describing what is intentionally not included (e.g., no server runtime) to prevent future reintroduction via accidental docs or scripts.

Acceptance for FR-001 through FR-007 is demonstrated when Success Criteria SC-001 through SC-004 are met.

### Ambiguities & Analysis Notes *(mandatory when present)*

- Scope definition: “Remove MCP server” includes removing server-specific deliverables and references; it does not require replacing it with any other server or interactive runtime.
- Cleanup level: “Repo cleaned up” is interpreted as removing MCP server-related files and references and ensuring remaining docs/scripts/tests are coherent and functional, without broad refactors unrelated to MCP server removal.
- Assumption: Existing non-server capabilities (semantic artifacts, validation, reports, examples) remain in place unless they exist solely to support MCP server operation.
- Non-goal: Introducing any new server/runtime experience is explicitly out of scope.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A repository-wide search for MCP server positioning/instructions yields no matches in primary documentation (README/quickstart/deployment docs), except where explicitly documenting that MCP server support is not provided.
- **SC-002**: The repository’s existing automated test workflow completes successfully on a clean checkout without requiring an MCP server.
- **SC-003**: A new reader can follow the “getting started” path from the README to perform at least one non-server semantic workflow without encountering server setup steps.
- **SC-004**: The repo contains no MCP server-specific deployment/start instructions (e.g., “start the server” workflows) in top-level operational docs.
