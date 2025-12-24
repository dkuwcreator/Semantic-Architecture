# Module: beta (Illustrative)

## Purpose / Intent

Demonstrate a consumer module that depends on `module-alpha` and highlights escalation when public interfaces change.

## Scope

### In-bounds

- Call `module-alpha` and produce a combined greeting output.

### Out-of-bounds

- Any complex logic, persistence, networking.

## Validation

- Manually run `stub.py` and confirm it prints a greeting.

## Drift checks

- If the consumer expectations change, update this README and `AGENT_INSTRUCTION.md`.
- If `module-alpha` changes, verify this module still matches its documented expectations.
