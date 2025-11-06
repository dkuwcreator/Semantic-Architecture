---
description: Project root semantic governance for humans and AI agents; intent before execution; bounded-context precedence; stewardship and traceability.
applyTo: '**'
---

# Semantic Governance — Project Root Instructions

This file defines project-wide semantic governance for humans and AI agents. It encodes intent before execution, establishes bounded-context precedence, and ensures stewardship and traceability across the Semantic Architecture (Project → Cluster → Module).

Accessibility: This file is human- and machine-readable; parsers may consume YAML front matter for validation.

> Metadata
- scope: project
- id: governance-root
- version: 1.0.0
- owners: ["@dkuwcreator"]
- last-updated: 2025-11-06
- links:
  - vision: docs/vision.md
  - semantic-project-model: docs/semantic-project-model.md
  - semantic-collaboration-model: docs/semantic-collaboration-model.md
  - glossary: docs/glossary.md

## 1. Purpose & scope
- Purpose: Provide root defaults for collaboration semantics, coding standards, and agent behavior.
- Scope: Applies to all work in this repository unless a nearer bounded context (cluster/module) narrows or overrides rules.
- Non-goals: Language-specific style minutiae (defer to module standards); deployment runbooks.

This file participates in the Semantic Evolution Loop — Perception → Reasoning → Action → Reflection → Verification → Evolution.

## 2. How to use this file
- When starting a task, skim this file first, then follow links in the front matter for context.
- If a module’s `semantic-instructions.md` defines stricter or more specific rules, follow the module.
- If guidance conflicts and can’t be resolved locally, use Escalation & Decisions below.

## 3. Semantic Architecture overview & precedence
- Structure: Project → Cluster → Module.
- Precedence (nearest-context wins): Module > Cluster > Project Root (.github) > External references.
- Overrides: Only narrower/more specific constraints may override broader defaults.

## 4. Context and intent anchors
Use these documents to ground meaning before mechanics:
- Vision: [docs/vision.md](../docs/vision.md)
- Project model: [docs/semantic-project-model.md](../docs/semantic-project-model.md)
- Collaboration model: [docs/semantic-collaboration-model.md](../docs/semantic-collaboration-model.md)
- Glossary (canonical terminology): [docs/glossary.md](../docs/glossary.md)

Guideline: Each substantive change should state the intent (problem, outcome) before the mechanics (edits, code, commands).

## 5. Behavior guidelines (agents and humans)
- Plan-first: For multi-step work, write a short plan and keep it updated as you proceed.
- Minimal diffs: Prefer the smallest change that satisfies intent; avoid drive-by refactors.
- Verification: For runnable code, add/adjust minimal tests; keep the build green.
- Progress cadence: Summarize after ~3–5 actions or when creating/editing >3 files.
- Tool/use: Use project-native tooling; do not introduce new dependencies without steward review.
- Privacy & security: Do not exfiltrate secrets or proprietary data; avoid linking to non-approved third-party content.
- Clarity: Prefer skimmable bullets, precise language, and explicit assumptions.

## 6. Output conventions
- Format: Markdown first; concise paragraphs and bullets; avoid heavy formatting unless needed.
- Code: Use fenced code blocks; include only necessary commands/snippets; prefer one command per line.
- Math: Use KaTeX ($inline$ or $$block$$) when math clarifies intent.
- Tests: Provide minimal runnable examples or tests for non-trivial code changes.
- Status: Clearly mark what changed and what’s next; avoid restating unchanged plans.

## 7. Coding standards & collaboration rules
- Style: Follow module or language-specific standards defined nearest to the code.
- Commits: Use Conventional Commits (e.g., `feat:`, `fix:`, `docs:`, `chore:`). Governance changes use `docs(governance):`.
- PRs: Keep PRs small and focused; link to related issues and context docs.
- Reviews: Changes affecting multiple modules require appropriate stewards in review.

## 8. Instruction precedence & override model
- Defaults live here; clusters/modules may specialize within their bounded contexts.
- An override must be strictly narrower or stricter; note the rationale and affected scope.
- Conflict policy: Nearest valid bounded context governs; unresolved conflicts escalate to stewardship.

## 9. Quality gates (green-before-done)
- Build: Must pass.
- Lint/Typecheck: Must pass.
- Tests: Add/update minimal tests; all tests must pass. For flaky checks, retry briefly (≤2) and document.

## 10. Privacy, security, and data handling
- Secrets: Never commit, echo, or paste credentials, tokens, or keys.
- Data boundaries: Assume all repository data is internal unless marked public.
- Licensing: Avoid including copyrighted third-party content without explicit license clearance.

## 11. Escalation & decision records
- Escalation path: Module steward → Cluster steward → Project owners (see `owners` in front matter).
- Record decisions: For exceptions or long-lived choices, capture the rationale and scope in a decision note (ADR/Semantic Decision) and link it from the PR description.
 - Example: ADR-001 — Cluster Boundaries

## 12. Maintenance & traceability
- Ownership: See `owners` in front matter; propose updates via PR and request review from owners.
- Versioning: Use SemVer in this file’s front matter; bump minor for guidance additions, patch for clarifications, major for breaking changes.
- Changelog: Maintain a brief history below; link to PRs.
 - Semantic Gravity: When modules or clusters exhibit high semantic gravity (heavy interconnections, long instructions, broad dependencies), trigger steward review and consider splitting into smaller modules.

## 13. Changelog
- 1.0.0 (2025-11-06): Initial root governance established; includes context links, precedence, behavior, output conventions, quality gates, and escalation.

## 14. Quick-reference checklists (appendix)

Agent checklist (before you start)
- Read Purpose & scope and Context anchors.
- Identify nearest bounded context and applicable overrides.
- Write a short plan; confirm assumptions.

Agent checklist (while working)
- Keep diffs minimal; summarize progress every 3–5 actions.
- Verify with tests for non-trivial changes; keep build green.
- Note any local overrides and rationale.

Human reviewer checklist (before merge)
- Intent before execution is clear; glossary terms are used consistently.
- Nearest-context rules are respected; overrides are justified and scoped.
- Quality gates are green; changes are small and traceable to issues/decisions.
