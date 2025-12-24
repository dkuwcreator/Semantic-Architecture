# Implementation Plan: Semantic Architecture Foundation Pack

**Branch**: `001-semantic-foundation-pack` | **Date**: 2025-12-23 | **Spec**: [specs/001-semantic-foundation-pack/spec.md](spec.md)
**Input**: Feature specification from `specs/001-semantic-foundation-pack/spec.md`

## Summary

Deliver a tool-agnostic “foundation pack” for Semantic Architecture by adding:

- A **normative core spec** (MUST/SHOULD/MAY rules) that defines Project/Cluster/Module, required module artifacts, escalation, and drift handling.
- **Reusable templates** (module `README.md`, module `AGENT_INSTRUCTION.md`, cluster overview template).
- A **minimal reference example** (1 project, 1 cluster, 2–3 modules) with **tiny illustrative code stubs** plus a documented drift scenario.
- A clearly labeled **non-normative Spec Kit adapter** under `adapters/spec-kit/`.

## Technical Context

**Language/Version**: Documentation-first repository; examples MAY include tiny illustrative code stubs (no runtime requirement).  
**Primary Dependencies**: N/A (Markdown, GitHub rendering).  
**Storage**: Filesystem only.  
**Testing**: Optional; prefer lightweight checks (e.g., link checks / markdown lint) if already present.  
**Target Platform**: GitHub (Markdown-first, readable in-browser).  
**Project Type**: Documentation/framework repository with optional reference tooling.  
**Performance Goals**: N/A.  
**Constraints**: Tool-agnostic core; Spec Kit content only in `adapters/spec-kit/` and explicitly non-normative; keep example minimal and comprehensible.  
**Scale/Scope**: Small, focused additions; avoid building a product.

## Constitution Check

*GATE: Must pass before implementation changes.*

- Tool-agnostic purity: core rules contain no tool/vendor dependencies; tooling guidance isolated to adapters.
- Bounded context: example modules are small; each module has `README.md` + `AGENT_INSTRUCTION.md`.
- Meaning-first parity: any behavior/intent changes include doc/instruction updates.
- Drift policy: drift definition and resolution steps are explicit; ambiguity triggers analysis before implementation.
- Review integrity: spec → plan → tasks → implement; reviewers validate boundaries and drift compliance.

## Proposed Repository Information Architecture

This feature establishes (or reinforces) the following top-level layout:

- `docs/` — normative core spec + supporting conceptual docs
- `templates/` — reusable, tool-agnostic templates
- `examples/` — minimal reference example (small enough to understand end-to-end)
- `adapters/` — optional tooling guidance (explicitly non-normative)

## File List (New/Updated) + Purpose

### Core spec (normative)

- **NEW** `docs/core-spec.md`
  - Normative definition of Project/Cluster/Module
  - Required module artifacts (`README.md`, `AGENT_INSTRUCTION.md`)
  - Agent collaboration/escalation rules
  - Drift definition + drift-handling workflow
  - Normative language (MUST/SHOULD/MAY)

- **UPDATED** `README.md`
  - Add clear “Start here” navigation:
    - Core spec (normative)
    - Templates
    - Example
    - Adapters (optional)
  - Clarify that the MCP server content is implementation/tooling, not the definition of the concept

### Templates (tool-agnostic)

- **NEW** `templates/semantic-module/README.md`
  - Generic module README template (intent, context, constraints, validation, drift checks)

- **NEW** `templates/semantic-module/AGENT_INSTRUCTION.md`
  - Generic agent instruction template (scope, guardrails, allowed changes, escalation triggers, verification)

- **NEW** `templates/semantic-cluster/README.md`
  - Generic cluster overview template (domain purpose, module index, boundaries, escalation rules, drift hotspots)

### Example (minimal, illustrative)

- **NEW** `examples/minimal-project/README.md`
  - Explains the example layout and states it is illustrative and non-normative

- **NEW** `examples/minimal-project/cluster-foundation/README.md`
  - Cluster overview for the example

- **NEW** `examples/minimal-project/cluster-foundation/module-alpha/README.md`
- **NEW** `examples/minimal-project/cluster-foundation/module-alpha/AGENT_INSTRUCTION.md`
- **NEW** `examples/minimal-project/cluster-foundation/module-alpha/stub.*`

- **NEW** `examples/minimal-project/cluster-foundation/module-beta/README.md`
- **NEW** `examples/minimal-project/cluster-foundation/module-beta/AGENT_INSTRUCTION.md`
- **NEW** `examples/minimal-project/cluster-foundation/module-beta/stub.*`

- **NEW (optional if 3 modules chosen)** `examples/minimal-project/cluster-foundation/module-gamma/...`

- **NEW** `examples/minimal-project/DRIFT_SCENARIO.md`
  - A concrete “before/after” drift scenario:
    - A meaning artifact claims behavior X
    - A stub implements behavior Y
    - A resolution section shows the update path to restore parity

> Note: `stub.*` can be a tiny code file (e.g., `.py`) or pseudo-code file (`.txt`). If code is used, it MUST be labeled illustrative and MUST NOT imply the core concept requires that language.

### Adapters (non-normative)

- **NEW** `adapters/spec-kit/README.md`
  - **NON-NORMATIVE** adapter guide
  - Shows how Spec Kit can support spec → plan → tasks workflows
  - Explicitly states the adapter does not change the core MUST/SHOULD/MAY rules

- **NEW (optional)** `adapters/spec-kit/workflow.md`
  - Example command flow and suggested folder conventions

### Contribution & review

- **NEW** `CONTRIBUTING.md`
  - Defines expected contribution flow: spec → plan → tasks → implement
  - Requires boundary integrity + drift checks during review

- **NEW** `.github/pull_request_template.md`
  - PR checklist for bounded context discipline + drift policy compliance

## Conventions

### Naming conventions

- Cluster/module directories and identifiers SHOULD use `kebab-case`.
- Names SHOULD be short and stable (avoid embedding implementation details).

### Required headings in templates

**Module `README.md` template MUST include**:

- Purpose / Intent
- Scope (in-bounds / out-of-bounds)
- Context & Assumptions
- Constraints
- Interfaces (inputs/outputs) (optional when docs-only)
- Validation (how to verify)
- Drift checks (what must stay in sync)

**Module `AGENT_INSTRUCTION.md` template MUST include**:

- Operating boundaries (what files/areas are editable)
- Allowed changes / forbidden changes
- Escalation triggers (when to escalate to cluster/project)
- Invariants (what must remain true)
- Verification steps (what to run/check)

**Cluster overview template SHOULD include**:

- Cluster purpose
- Module index (table of modules + responsibilities)
- Cross-module boundaries
- Escalation guidance
- Drift hotspots (common drift risks)

### Drift policy placement + usage

- Drift policy is defined normatively in `docs/core-spec.md`.
- Templates include a “Drift checks” section to operationalize the policy.
- The example includes `DRIFT_SCENARIO.md` to demonstrate drift detection and resolution.
- Review checklist requires confirming:
  - meaning artifacts updated alongside behavior changes
  - no contradictions between core spec, templates, examples, and code

## Migration Steps (Reusing Existing Repo Documents)

Goal: Preserve existing content while introducing a clear normative core.

1. **Introduce `docs/core-spec.md` as the normative anchor**.
   - Keep existing documents as supporting context.
   - Add cross-links from core spec to:
     - `docs/semantic-project-model.md`
     - `docs/semantic-collaboration-model.md`
     - `docs/glossary.md`
     - `docs/vision.md`

2. **Reclassify existing docs by intent (without deleting content)**:
   - Treat `docs/vision.md` as conceptual (“why”).
   - Treat `docs/semantic-project-model.md` and `docs/semantic-collaboration-model.md` as deep dives that the core spec references.
   - Ensure terminology matches the core spec (especially required artifacts).

3. **Update `README.md` navigation**:
   - Add “Core spec (normative)” as the top entry point.
   - Keep MCP server quickstart links, but clearly label them as optional tooling/implementation.

4. **Add templates and example**:
   - Templates become copy/paste entrypoints.
   - Example becomes a minimal “reference implementation” of structure and drift policy.

## Step-by-Step Implementation Plan (Task-Ready)

1. Create `docs/core-spec.md` (normative) with MUST/SHOULD/MAY rules.
2. Update `README.md` to add top-level navigation and distinguish core vs adapters/tooling.
3. Create templates:
   - `templates/semantic-module/README.md`
   - `templates/semantic-module/AGENT_INSTRUCTION.md`
   - `templates/semantic-cluster/README.md`
4. Create example skeleton under `examples/minimal-project/`:
   - 1 cluster, 2–3 modules, each with required artifacts
   - add tiny illustrative code stubs (explicitly labeled non-normative)
5. Add `examples/minimal-project/DRIFT_SCENARIO.md` demonstrating drift and resolution.
6. Add `adapters/spec-kit/README.md` (explicitly non-normative), plus optional `workflow.md`.
7. Add contribution artifacts:
   - `CONTRIBUTING.md`
   - `.github/pull_request_template.md`
8. Consistency pass:
   - Ensure terms match core spec across docs/templates/example
   - Ensure all adapter docs are labeled non-normative
   - Ensure paths and links work in GitHub rendering

## Complexity Tracking

No constitution violations expected. If any emerge:

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --- | --- | --- |
| N/A | N/A | N/A |
