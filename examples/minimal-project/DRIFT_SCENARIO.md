# Drift Scenario (Illustrative)

This scenario is **illustrative** and **NON-NORMATIVE**.

The goal is to show how drift is detected and resolved:

- **Meaning**: what the module docs claim.
- **Behavior**: what the stub code does.

## Scenario

### Before (drift)

1. `module-alpha/README.md` claims `greet()` returns **"Hi, {name}"**.
2. `module-alpha/stub.py` actually returns **"Hello, {name}!"**.

This is semantic drift (meaning ≠ behavior).

### Detect

- Compare `module-alpha/README.md` against `module-alpha/stub.py` behavior.
- Identify the exact conflicting statements.

### Resolve

Choose one:

- If "Hello" is intended: update `module-alpha/README.md` (and `AGENT_INSTRUCTION.md` if needed) to match the stub.
- If "Hi" is intended: update `module-alpha/stub.py` to match the docs.

### Prevent reintroduction

- Add an explicit verification step in `module-alpha/README.md` or `AGENT_INSTRUCTION.md`.
- Keep the module small and bounded so parity is easy to maintain.

See the drift workflow in [docs/core-spec.md](../../docs/core-spec.md).
