description: Plan changes using the Semantic Evolution Loop with explicit scope, impact, and validation.
mode: instructions
---

# Purpose
Ensure changes are designed with intent, bounded scope, and verifiable outcomes before edits.

> Metadata
- id: evolution-planning
- name: Evolution Planning
- scope: project
- owners: ["@dkuwcreator"]
- version: 1.0.0
- last-updated: 2025-11-06

Inputs
- intentStatement (string, required): What you want to achieve and why
- targetScope (string, required): module|cluster|project
- constraints (array<string>, optional): Budget, time, technical constraints
- successCriteria (array<string>, required): Acceptance criteria
- suspectedImpact (array<string>, optional): Modules/clusters likely affected
- timeline (string, optional): Optional timeline or priority

Outputs
- plan (markdown): Loop-structured plan
- impactMap (markdown): List of affected modules/tests and dependencies
- validationChecklist (markdown): Tests, gates, and sign-offs required
- adrStub (markdown): ADR/Semantic Decision draft with context and consequences

Safety
- boundedContext: true
- writePolicy: read-only
- escalation: If plan alters contracts across modules, require cluster steward approval and ADR.

References
- governance: ../../.github/copilot-instructions.md
- vision: ../../docs/vision.md
- projectModel: ../../docs/semantic-project-model.md
- collaborationModel: ../../docs/semantic-collaboration-model.md
- glossary: ../../docs/glossary.md

# Plan structure (Semantic Evolution Loop)
- Perception: Current state summary, pain points, and constraints
- Reasoning: Options considered, trade-offs, chosen approach
- Action: Minimal steps, ordered for safety (tests-first when altering behavior)
- Reflection: Documentation updates (about.md, semantic-instructions.md)
- Verification: Quality gates (build/lint/tests), success criteria
- Evolution: Rollout, follow-ups, and escalation path

# Deliverables
- plan: Concise, skimmable bullets with explicit targetScope
- impactMap: Affected modules, contracts, and tests
- validationChecklist: What must be green-before-done
- adrStub: Title, context, decision, consequences, links

# Success criteria
- Meaning before mechanics; accept plan only when validation is clear.
- Bounded to the smallest sufficient scope; escalate only when necessary.
- Stewardship acknowledged with clear sign-offs.
