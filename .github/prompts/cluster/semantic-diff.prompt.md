description: Summarize changes between two refs as intent, contract updates, impact, and validation status.
mode: instructions
---

# Purpose
Provide an intent-level diff to augment line diffs with semantic context.

> Metadata
- id: semantic-diff
- name: Semantic Diff
- scope: cluster
- owners: ["@dkuwcreator"]
- version: 1.0.0
- last-updated: 2025-11-06

Inputs
- scopePath (path, required): Module or cluster directory path
- beforeRef (string, required): Git ref or SHA (before)
- afterRef (string, required): Git ref or SHA (after)
- contractFilePath (path, optional): Path to semantic-instructions.md (defaults to local)

Outputs
- summary (markdown): Intent Change, Contract Update, Impact, Validation
- bcAssessment (string): backward-compatibility: low|medium|high
- referencedTests (array<string>): Tests verifying the changed behaviors
- followUps (array<string>): Docs or ADRs to update

Safety
- boundedContext: true
- writePolicy: read-only
- escalation: If impact spans clusters, escalate to project steward for integration planning.

References
- governance: ../../.github/copilot-instructions.md
- vision: ../../docs/vision.md
- projectModel: ../../docs/semantic-project-model.md
- collaborationModel: ../../docs/semantic-collaboration-model.md
- glossary: ../../docs/glossary.md

# Output format
- Intent Change: human-readable capability-summary
- Contract Update: invariants added/removed/modified
- Impact: affected modules/files and surface areas
- Validation: tests added/changed; status
- Backward compatibility: low|medium|high with rationale

# Steps
1. Parse contract and public surfaces at before/after.
2. Detect changes in invariants and exported interfaces.
3. Map changes to tests; note gaps.
4. Summarize impact and BC level; propose follow-ups.
