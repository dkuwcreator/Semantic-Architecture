# Semantic Module Agent Instructions (Template)

## Operating boundaries

### In scope

List the files/directories that are in-bounds for changes.

### Out of scope

List files/directories that MUST NOT be changed by default.

## Allowed changes

Describe allowed change types (e.g., bugfix, refactor-safe).

## Forbidden changes

Describe forbidden change types (e.g., breaking interface changes) unless explicitly approved.

## Escalation triggers

Escalate to cluster/project scope when:

- A change impacts another module’s responsibilities or interfaces.
- A change alters cross-module contracts/invariants.
- A change requires redefining cluster boundaries or project-level intent.

## Invariants / contracts

List invariants that MUST remain true.

## Verification steps

List what to run/check before claiming completion.

See the normative rules in [docs/core-spec.md](../../docs/core-spec.md).
