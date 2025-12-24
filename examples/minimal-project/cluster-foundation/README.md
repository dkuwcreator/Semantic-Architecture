# Cluster: foundation (Illustrative)

This cluster exists only to demonstrate structure and boundaries.

- This cluster is **illustrative** and **NON-NORMATIVE**.
- The normative rules live in [docs/core-spec.md](../../../docs/core-spec.md).

## Module index

| Module | Responsibility | Out of scope |
|--------|----------------|--------------|
| module-alpha | Provides a tiny greeting function and demonstrates meaning-first parity. | Any persistence, networking, or cross-module coordination. |
| module-beta | Consumes module-alpha and demonstrates escalation when interfaces change. | Any business logic beyond the example. |
