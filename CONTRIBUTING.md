# Contributing to Semantic Architecture

This repository is maintained under the governance in [.specify/memory/constitution.md](.specify/memory/constitution.md).

## Contribution flow (required for substantive changes)

A **substantive change** is any change that alters meaning, behavior, boundaries, contracts, or interfaces.

For substantive changes, follow this order:

1. **Spec**: define scenarios, requirements, success criteria (use `specs/<feature>/spec.md`).
2. **Plan**: record analysis, design choices, constitution check (use `specs/<feature>/plan.md`).
3. **Tasks**: define ordered work items with file paths (use `specs/<feature>/tasks.md`).
4. **Implement**: change docs/tests/code and validate.

If artifacts conflict or anything is unclear, do **analysis first** before implementing.

## Drift and boundary integrity (mandatory)

This project treats inconsistencies between meaning artifacts and behavior as **semantic drift**.

When you change behavior or intent:

- Update the relevant meaning artifacts (at minimum `README.md` and `AGENT_INSTRUCTION.md` for the affected module).
- Ensure related supporting docs and templates remain consistent.
- Add or update validation steps (tests/checks) so drift is harder to reintroduce.

## Tool-agnostic core vs adapters

- Core normative guidance lives in `docs/`.
- Tool-specific guidance belongs under `adapters/` and must be explicitly labeled **NON-NORMATIVE**.
- Adapters must not redefine or contradict the core specification.

## Review checklist (what reviewers must confirm)

Reviewers should block merges if any of the following are not true:

- Scope is bounded to the smallest appropriate context (module → cluster → project).
- Meaning artifacts remain in parity with behavior.
- No contradictions between core spec, templates, examples, and implementation.
- Validation steps are appropriate for the change and are run (when applicable).

## Suggested commit message convention

Prefer commit messages that indicate semantic scope, for example:

- `[docs] Add normative core spec`
- `[templates] Add module templates`
- `[examples/minimal-project] Add drift scenario`

(Exact conventions may evolve; prioritize clarity and reviewability.)
