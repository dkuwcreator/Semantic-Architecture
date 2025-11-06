# Reusable Prompt Workflows (.github/prompts)

This folder contains reusable, bounded-context prompt workflows aligned with the Semantic Architecture. Each prompt is human- and machine-readable and includes YAML metadata for discoverability.

## Conventions

- One prompt per file; kebab-case names ending with `.prompt.md`.
- Scopes: `module`, `cluster`, `project` (declared in file metadata/body; YAML header is minimal).
- Outputs are proposals by default (diffs/patches/test lists). Applying changes requires steward review per `.github/copilot-instructions.md`.
- References in each prompt point to: governance, vision, project/collaboration models, and glossary.

## Index

### Module

- `module/scaffold-semantic-module.prompt.md`
  - Purpose: Scaffold a new self-describing module (docs + contract + tests + placeholder code).
  - Inputs: moduleName, parentClusterPath, language, owners, shortDescription, initialCapabilities, invariants, validationTests.
- `module/review-semantic-drift.prompt.md`
  - Purpose: Detect and propose fixes for module-level semantic drift.
  - Inputs: targetPath, changedFiles, referencedTests, diffRange.
- `module/validate-invariants.prompt.md` (optional)
  - Purpose: Ensure every invariant has explicit test coverage.
  - Inputs: modulePath, invariants, referencedTests.

### Cluster

- `cluster/review-semantic-drift.prompt.md`
  - Purpose: Aggregate module drift and propose coordinated fixes within a cluster.
  - Inputs: clusterPath, modules, diffRange.
- `cluster/semantic-diff.prompt.md` (optional)
  - Purpose: Provide intent-level diff across refs for a module or cluster.
  - Inputs: scopePath, beforeRef, afterRef, contractFilePath.

### Project

- `project/evolution-planning.prompt.md`
  - Purpose: Plan changes using the Semantic Evolution Loop with bounded scope, validation, and stewardship.
  - Inputs: intentStatement, targetScope, constraints, successCriteria, suspectedImpact, timeline.

## Stewardship and Safety

- Each prompt names its intended steward in a Metadata block in the body.
- Safety policies:
  - `boundedContext: true` – prompts operate in their declared scope.
  - `writePolicy` – proposal-only by default (`read-only` or `propose-diff` or `scaffold-only`).
  - `escalation` – when contracts or shared interfaces change, require steward approval and ADR.

## References

- Governance: `.github/copilot-instructions.md`
- Vision: `docs/vision.md`
- Project Model: `docs/semantic-project-model.md`
- Collaboration Model: `docs/semantic-collaboration-model.md`
- Glossary: `docs/glossary.md`
