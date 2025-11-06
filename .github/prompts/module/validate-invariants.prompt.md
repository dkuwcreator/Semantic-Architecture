description: Check that declared invariants have direct test coverage and evidence.
mode: instructions
---

# Purpose
Ensure every declared invariant has a clear line of evidence in tests and documentation.

> Metadata
- id: validate-invariants
- name: Validate Invariants
- scope: module
- owners: ["@dkuwcreator"]
- version: 1.0.0
- last-updated: 2025-11-06

Inputs
- modulePath (path, required): Module directory path
- invariants (array<string>, optional): Override invariants list (falls back to semantic-instructions.md)
- referencedTests (array<string>, optional): Known tests covering invariants

Outputs
- validationMatrix (markdown): Invariant → evidence → status
- gaps (array<object>): Missing or weak coverage items with recommendations
- patch (patch): Optional patch to add/align tests or doc references

Safety
- boundedContext: true
- writePolicy: propose-diff
- escalation: If invariants are unclear or contradictory, require steward clarification and ADR update.

References
- governance: ../../.github/copilot-instructions.md
- vision: ../../docs/vision.md
- projectModel: ../../docs/semantic-project-model.md
- collaborationModel: ../../docs/semantic-collaboration-model.md
- glossary: ../../docs/glossary.md

# Steps
1. Read invariants from `semantic-instructions.md` (or provided list).
2. Map each invariant to concrete tests and code paths.
3. Report status: pass/fail/unknown. Propose minimal test additions if gaps exist.
4. If invariants are missing or ambiguous, recommend updates to the contract first.

# Success criteria
- Test coverage is explicit for each invariant.
- Proposed changes are minimal and local to the module.
- Contract and tests remain synchronized.
