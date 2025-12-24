# Module: alpha (Illustrative)

## Purpose / Intent

Provide a tiny, stable function that returns a greeting string.

## Scope

### In-bounds

- Provide `greet(name: str) -> str`.

### Out-of-bounds

- Any I/O, network calls, persistence, or configuration.

## Constraints

- Keep the API intentionally tiny.
- Keep the behavior fully described by this README.

## Validation

- Manually run `stub.py` and confirm output is a greeting string.

## Drift checks

- If `greet()` behavior changes, update this README and `AGENT_INSTRUCTION.md`.
- If the public signature changes, escalate to the cluster README because it impacts consumers.
