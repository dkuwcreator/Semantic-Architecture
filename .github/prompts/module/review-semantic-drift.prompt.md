description: Detect and propose fixes for divergence between a module’s code, docs, and semantic contract.
mode: instructions
---

# Purpose
Preserve each module as a Living Knowledge Cell by surfacing and repairing semantic drift.

> Metadata
- id: review-semantic-drift
- name: Review Semantic Drift
- scope: module
- owners: ["@dkuwcreator"]
- version: 1.0.0
- last-updated: 2025-11-06

Inputs
- targetPath (path, required): Module directory path
- changedFiles (array<string>, optional): Subset of files to focus on
- referencedTests (array<string>, optional): Known tests validating invariants
- diffRange (string, optional): Git range (e.g., origin/main..HEAD)

Outputs
- driftReport (markdown): Findings with severity and evidence
- fixes (array<object>): Ranked fix suggestions with rationale
- patch (patch): Minimal combined patch for docs/tests/code
- riskLevel (string): low|medium|high

Safety
- boundedContext: true
- writePolicy: propose-diff
- escalation: If invariants or public interfaces change, require steward review and an ADR reference.

References
- governance: ../../.github/copilot-instructions.md
- vision: ../../docs/vision.md
- projectModel: ../../docs/semantic-project-model.md
- collaborationModel: ../../docs/semantic-collaboration-model.md
- glossary: ../../docs/glossary.md

# Drift categories
- Contract drift: `semantic-instructions.md` invariants vs actual behavior/tests
- Documentation drift: `about.md` vs code interfaces/exported behaviors
- Test drift: tests missing for declared invariants or stale test references
- Link drift: broken links to docs, glossary, or related modules

# Steps (Semantic Evolution Loop)
1. Perception
   - Read `semantic-instructions.md` contract and referenced tests.
   - Parse code public surface (functions/exports) and compare to docs.
2. Reasoning
   - Classify mismatches by severity (low/medium/high).
   - Identify the smallest change that realigns meaning.
3. Action (proposal only)
   - Produce a single minimal patch to update docs/tests/code.
   - Prefer test-first if behavior changes.
4. Reflection
   - Ensure glossary terms are used consistently.
   - Update `semantic-instructions.md` when contracts change.
5. Verification
   - List tests that should pass; recommend retries for flake.
6. Evolution
   - If cross-module effects detected, escalate to cluster steward before changes.

# Output format
- driftReport: Table or bullets with file refs and line spans.
- fixes: Each item contains {change, rationale, impact, files, risk}.
- patch: Unified diff covering only the module.
- riskLevel: Overall assessment.

# Success criteria
- Meaning restored before mechanics: docs/contracts lead, tests align, then code.
- Minimal diffs; bounded to the module.
- Clear steward checkpoints for risky changes.
