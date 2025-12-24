# Semantic Architecture Core Specification (Normative)

This document defines the **normative** rules for Semantic Architecture.

- **Normative** statements use MUST / MUST NOT / SHOULD / MAY.
- Supporting/conceptual documents may elaborate, but **must not contradict** this specification.

## 1. Core model

### 1.1 Semantic Project

A **Semantic Project** is the repository-level unit that contains one or more Semantic Clusters.

A Project:

- MUST define or link to the project’s overarching intent and boundaries.
- SHOULD provide an entrypoint for navigation across the architecture.

### 1.2 Semantic Cluster

A **Semantic Cluster** is a bounded domain/subsystem grouping of related Semantic Modules.

A Cluster:

- SHOULD describe its domain purpose and boundaries.
- SHOULD enumerate contained modules and their responsibilities.

### 1.3 Semantic Module

A **Semantic Module** is the smallest self-contained unit of meaning that can be understood in isolation.

A Module:

- MUST have a single, clear responsibility.
- MUST remain small enough for a single human or single agent to understand without hidden external context.

## 2. Required meaning artifacts

### 2.1 Module artifacts (non-negotiable)

Every Semantic Module MUST include:

- `README.md` (human intent, context, constraints)
- `AGENT_INSTRUCTION.md` (operating rules, guardrails, boundaries)

These are the module’s **meaning artifacts** and are treated as first-class.

### 2.2 Recommended artifacts at higher layers

At the Cluster and Project layers:

- `README.md` SHOULD exist to describe purpose, scope, and navigation.
- `AGENT_INSTRUCTION.md` MAY exist to define automation/agent boundaries when applicable.

If a repository chooses to enforce `AGENT_INSTRUCTION.md` at Cluster/Project levels, it MUST do so consistently across the repository and document the rule in this core spec or an explicitly referenced normative addendum.

## 3. Scope and escalation

Changes MUST stay within the smallest possible scope that contains the change:

- Module → Cluster → Project

Escalation triggers (non-exhaustive):

- A change impacts another module’s responsibilities or interfaces.
- A change alters cross-module contracts/invariants.
- A change requires redefining cluster boundaries or project-level intent.

## 4. Meaning-first parity

Documentation and implementation (when present) are equal artifacts.

- Any change that affects behavior, intent, scope, invariants, or interfaces MUST update the relevant meaning artifacts.
- If meaning artifacts and implementation disagree, this is **drift** and MUST be resolved before merge.

## 5. Drift management (analysis-first)

**Drift** is any inconsistency between meaning artifacts, templates, examples, and implementation.

Minimum drift checks for any substantive change:

- Verify the affected module’s `README.md` and `AGENT_INSTRUCTION.md` still match reality.
- Verify any referenced contracts/invariants are still true.
- If code exists, verify tests and/or validation steps cover the declared behavior.

Drift resolution order:

1. Identify the conflicting statements.
2. Decide the intended meaning (escalate to a human steward when needed).
3. Update artifacts so intent and behavior converge (docs/instructions/tests/code).
4. Add or update validation steps so the drift is harder to reintroduce.

## 6. Tool-agnostic purity

The Semantic Architecture core model MUST remain independent of any specific tool, vendor, API, IDE, or workflow product.

- Normative guidance MUST live in `docs/` and MUST avoid tool- or vendor-specific instructions.
- Tool-specific guidance MAY exist only under `adapters/` and MUST be explicitly labeled **NON-NORMATIVE**.
- Examples MAY include tiny code stubs, but they MUST be explicitly labeled illustrative and **NON-NORMATIVE**.

## 7. Naming conventions

- Cluster and module directory names SHOULD use `kebab-case`.
- Names SHOULD be short and stable (avoid encoding implementation details).

## 8. Compliance and review

For substantive changes, repositories SHOULD follow: **spec → plan → tasks → implement**.

Reviewers MUST verify:

- Bounded scope and correct escalation.
- Drift compliance (meaning artifacts updated; contradictions removed).
- Validation steps are appropriate and run when applicable.
