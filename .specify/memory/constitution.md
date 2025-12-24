<!--
SYNC IMPACT REPORT

- Version change: N/A (template) → 1.0.0
- Modified principles: N/A (template) → Tool-Agnostic Purity; Bounded Context Discipline;
  Meaning-First Parity; Drift Management (Analysis-First); Spec-Driven Change + Review Integrity
- Added sections: Structure & Writing Standards; Contribution & Review Workflow; Governance
- Removed sections: N/A
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
  - ✅ .specify/templates/checklist-template.md
  - ⚠ N/A: .specify/templates/commands/*.md (no command templates found in this repo)
- Deferred items: None
-->

# Semantic Architecture Constitution

## Core Principles

### I. Tool-Agnostic Purity (NON-NEGOTIABLE)

The Semantic Architecture core model (Project → Cluster → Module) MUST remain independent of any
specific AI tool, vendor, API, IDE, or workflow product.

- Core normative guidance MUST live in `docs/` and MUST avoid tool- or vendor-specific instructions.
- Tool-specific guidance MAY exist only under `adapters/` and MUST be explicitly **non-normative**.
- Tooling MAY accelerate work, but it MUST NOT define the concept; the concept must remain portable.
- When writing examples, authors MUST distinguish:
  - **Normative**: what the architecture requires.
  - **Adapter**: how a specific tool implements or automates the requirement.

### II. Bounded Context Discipline

Every Semantic Module MUST be small enough for a single person or a single agent to fully understand
without relying on hidden, external context.

Non-negotiable module artifacts:

- Every module MUST include `README.md` (human intent, context, constraints).
- Every module MUST include `AGENT_INSTRUCTION.md` (AI operating rules, guardrails, boundaries).

Boundary rules:

- Changes MUST stay within the smallest possible scope (module → cluster → project), escalating only
  when required by contracts, invariants, or cross-cutting impact.
- If a module grows beyond a single-context comprehension window, it MUST be split.
- Any example module included in this repository MUST follow the same rules.

### III. Meaning-First Parity

Documentation and code (when present) are equal artifacts.

- Any change that affects behavior, intent, scope, invariants, or interfaces MUST update the relevant
  meaning artifacts (at minimum the module `README.md` and `AGENT_INSTRUCTION.md`).
- PRs MUST be evaluated for semantic completeness, not only runtime correctness.
- If documentation and implementation disagree, this is drift and MUST be resolved before merge.

### IV. Drift Management (Analysis-First)

This repository treats inconsistencies between meaning artifacts and implementation/examples as
semantic drift.

Drift policy:

- Drift MUST be detected and fixed as part of normal development.
- When ambiguity is present (unclear requirement, conflicting artifacts, missing boundaries), an
  explicit **analysis step** MUST happen before implementation.

Minimum drift checks for any substantive change:

- Verify the affected module's `README.md` and `AGENT_INSTRUCTION.md` still match reality.
- Verify any referenced contracts/invariants are still true.
- If code exists, verify tests and/or validation steps cover the declared behavior.

Drift resolution order:

1. Identify the conflicting statements (quote the exact doc/instruction text).
2. Decide the intended meaning with a human reviewer/steward when needed.
3. Update artifacts so intent and behavior converge (docs/instructions/tests/code).
4. Add or update validation steps so the same drift is harder to reintroduce.

### V. Spec-Driven Change + Review Integrity

All substantive changes MUST follow spec-driven artifacts in order:

1. **Spec**: user scenarios, requirements, success criteria.
2. **Plan**: analysis/research, design choices, constitution gates.
3. **Tasks**: ordered work items with file paths.
4. **Implement**: code/docs changes with validation.

Review requirements:

- Reviewers MUST validate boundary integrity (module scope and escalation correctness).
- Reviewers MUST validate drift compliance (meaning artifacts updated, contradictions removed).
- If the plan/spec contains `NEEDS CLARIFICATION`, implementation MUST NOT proceed without recorded
  resolution.

## Structure & Writing Standards

### Repository layout (normative)

- Core concept/specification MUST live in `docs/`.
- Reusable templates MUST live in `templates/`.
- Example modules MUST live in `examples/`.
- Tool-specific integrations MUST live in `adapters/` and are **non-normative**.

Note: This repository also contains implementation code (e.g., validation and servers). Those are
allowed, but the Semantic Architecture concept MUST remain portable even without them.

### Module template (normative)

Every Semantic Module directory MUST include:

`README.md`

- Intent: what problem this module solves and why.
- Context: assumptions, dependencies, and boundaries.
- Constraints: what this module MUST NOT do.
- Validation: how to verify correctness (tests, checks, examples).

`AGENT_INSTRUCTION.md`

- Scope boundaries: what files are in-bounds vs out-of-bounds.
- Safe change policy: allowed changes, forbidden changes, escalation triggers.
- Invariants/contracts: what MUST remain true.
- Verification steps: what to run/check before claiming completion.

### Writing standards (normative)

- Core specs and module artifacts MUST use concise, explicit language.
- Use normative terms:
  - MUST / MUST NOT for non-negotiables
  - SHOULD for strong defaults with explicit rationale
  - MAY for optional guidance
- Prefer declarative, testable statements over vague guidance.

### Adapters (explicitly non-normative)

`adapters/` may include:

- Tool-specific workflows (e.g., Spec Kit usage), automation scripts, CI wiring.
- Integration guidance for context providers/servers.

Adapter documents MUST include a header stating they are non-normative and MUST NOT redefine core
principles.

## Contribution & Review Workflow

### Required flow for substantive changes

- Substantive change = any change that alters meaning, behavior, boundaries, or contracts.
- Substantive changes MUST follow: spec → plan → tasks → implement.

### Ambiguity handling (mandatory)

- If requirements are ambiguous or artifacts conflict, contributors MUST produce an analysis note in
  the plan before implementing.
- The analysis MUST capture: competing interpretations, chosen interpretation, and why.

### Review gates (mandatory)

Reviewers MUST confirm:

- Bounded scope: change contained to smallest appropriate layer.
- Module completeness: affected modules still have `README.md` and `AGENT_INSTRUCTION.md` and they are
  updated.
- Drift resolved: no contradictions between docs, instructions, examples, and code.
- Validation updated/run: checks/tests/verification steps still match the declared behavior.

### Rules of engagement (humans + agents)

- Work inside the smallest bounded context that contains the change.
- Read `README.md` + `AGENT_INSTRUCTION.md` before editing anything.
- If something is unclear: stop and write analysis before implementing.
- Keep docs and behavior in parity; fix drift immediately.
- Put tool-specific steps only in `adapters/` and treat them as non-normative.

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

This constitution is the highest-level normative governance for the repository.

Amendment procedure:

- Amendments MUST be proposed via PR.
- The PR MUST include:
  - the rationale for the change,
  - an impact assessment (what existing practices/docs/templates must change), and
  - migration steps if the amendment is behaviorally incompatible.

Versioning policy:

- Semantic versioning applies to this constitution:
  - MAJOR: backward-incompatible governance changes or removals.
  - MINOR: new principles/sections or materially expanded constraints.
  - PATCH: clarifications and non-semantic refinements.

Compliance expectations:

- Every spec/plan MUST include a constitution check.
- Reviewers MUST block merges that violate non-negotiable principles.
- Tool-specific workflows MUST remain isolated to `adapters/`.

**Version**: 1.0.0 | **Ratified**: 2025-12-23 | **Last Amended**: 2025-12-23
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
