# Minimal Project (Illustrative Example)

This directory contains a tiny reference example to demonstrate the Semantic Architecture structure.

- This example is **illustrative** and **NON-NORMATIVE**.
- The normative rules live in [docs/core-spec.md](../../docs/core-spec.md).

## Structure

- `cluster-foundation/` — a single cluster with two modules
- Each module contains the required meaning artifacts:
  - `README.md`
  - `AGENT_INSTRUCTION.md`

## What to look for

- Clear boundaries per module.
- Explicit escalation triggers.
- A documented drift scenario in `DRIFT_SCENARIO.md`.

See the drift workflow in [docs/core-spec.md](../../docs/core-spec.md).
