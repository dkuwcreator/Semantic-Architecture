# Agent Instructions: module-beta (Illustrative)

This module is **illustrative** and **NON-NORMATIVE**.

Normative rules: [docs/core-spec.md](../../../../docs/core-spec.md).

## Operating boundaries

### In scope

- `examples/minimal-project/cluster-foundation/module-beta/**`

### Out of scope

- Changing `module-alpha` directly.

## Allowed changes

- Small refactors that preserve behavior.
- Documentation updates to maintain parity.

## Forbidden changes

- Introducing new dependencies or expanding scope.

## Escalation triggers

Escalate to the cluster when:

- `module-alpha` interface changes affect this module.
- You need to change cross-module boundaries.

## Invariants

- The output remains a greeting derived from `module-alpha`.

## Verification steps

- Run `stub.py` and confirm it prints a greeting.
