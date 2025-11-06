description: Aggregate module-level drift in a cluster and propose coordinated, minimal fixes.
mode: instructions
---

# Purpose
Coordinate semantic integrity across modules within one domain while keeping changes local and minimal.

> Metadata
- id: review-semantic-drift-cluster
- name: Review Semantic Drift (Cluster)
- scope: cluster
- owners: ["@dkuwcreator"]
- version: 1.0.0
- last-updated: 2025-11-06

Inputs
- clusterPath (path, required): Cluster directory path
- modules (array<string>, optional): Subset of module directories to include
- diffRange (string, optional): Git range (e.g., origin/main..HEAD)

Outputs
- driftDashboard (markdown): Cluster-wide drift summary with per-module rollups
- prioritizedFixes (array<object>): Ordered fixes that minimize cross-module risk
- patches (array<patch>): Set of minimal patches per module
- escalationNotes (markdown): When to escalate to project level

Safety
- boundedContext: true
- writePolicy: propose-diff
- escalation: If shared contracts/interfaces are impacted, require project-level ADR and approvals.

References
- governance: ../../.github/copilot-instructions.md
- vision: ../../docs/vision.md
- projectModel: ../../docs/semantic-project-model.md
- collaborationModel: ../../docs/semantic-collaboration-model.md
- glossary: ../../docs/glossary.md

# Steps
1. Perception: Collect each module’s `semantic-instructions.md`, `about.md`, exports/interfaces, and tests.
2. Reasoning: Identify cross-module inconsistencies, shared contracts, and dependency edges.
3. Action (proposals): Prepare independent minimal patches per module; avoid broad refactors.
4. Reflection: Reconfirm terminology with the glossary and update docs where needed.
5. Verification: Outline tests to run per module and cluster-level interactions.
6. Evolution: Propose sequencing and merge order; add escalation notes when shared interfaces change.

# Success criteria
- Fix proposals remain per-module unless an interface is genuinely shared.
- Clear rollout plan and checklists; ADR references when contracts are adjusted.
