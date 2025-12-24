# Spec Kit Adapter (NON-NORMATIVE)

This document is **NON-NORMATIVE**.

It describes one possible way to use Spec Kit to support the workflow described by the Semantic Architecture core specification.

- The normative rules live in `docs/core-spec.md`.
- This adapter does not change any MUST/SHOULD/MAY rules.

## Suggested workflow

1. Create or update a feature spec under `specs/<feature>/spec.md`.
2. Record analysis and design decisions in `specs/<feature>/plan.md`.
3. Maintain an ordered task list in `specs/<feature>/tasks.md`.
4. Implement changes while keeping meaning artifacts in parity.

## Guardrails

- Do not introduce tool-specific language into `docs/`.
- Keep tool-specific guidance confined to `adapters/`.
- Treat drift (meaning ≠ behavior) as a blocking issue.
