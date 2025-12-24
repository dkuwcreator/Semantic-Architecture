# Agent Instructions: module-alpha (Illustrative)

This module is **illustrative** and **NON-NORMATIVE**.

Normative rules: [docs/core-spec.md](../../../../docs/core-spec.md).

## Operating boundaries

### In scope

- `examples/minimal-project/cluster-foundation/module-alpha/**`

### Out of scope

- Any other modules, including `module-beta`.

## Allowed changes

- Small refactors that preserve `greet(name: str) -> str`.
- Documentation updates to maintain parity.

## Forbidden changes

- Changing the `greet()` signature without cluster-level escalation.

## Escalation triggers

Escalate to the cluster when:

- `greet()` signature changes.
- You need cross-module coordination.

## Invariants

- `greet()` always returns a string.

## Verification steps

- Run `stub.py` and confirm it prints a greeting.
