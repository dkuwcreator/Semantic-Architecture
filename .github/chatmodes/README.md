# Chat Modes (.github/chatmodes)

Role-based AI personas aligned with the Semantic Collaboration Model. Each mode is human- and machine-readable, with minimal YAML in the header and detailed Metadata in the body.

## Conventions

- One mode per file; kebab-case names ending with `.mode.md`.
- Minimal YAML: `description`, `mode: instructions`; rich fields live in a top-level Metadata section.
- Each mode declares: role, scope, version, last-updated, owners, tools (prompts + optional integrations), behavior, escalation, references, boundaries.
- All modes inherit governance from `.github/copilot-instructions.md`.

## Index

### Module

- `module/module-agent.mode.md`
  - Role: Module Agent — operates within a single Semantic Module, using module prompts.

### Cluster

- `cluster/cluster-steward.mode.md`
  - Role: Cluster Steward — coordinates related modules; proposes per-module minimal patches.

### Project

- `project/project-architect.mode.md`
  - Role: Project Architect — maintains cross-cluster coherence; plans and ADRs.

### Optional

- `optional/evolution-reviewer.mode.md` — intent-level reviews for plans/diffs.
- `optional/semantic-maintenance-agent.mode.md` — continuous drift detection and small fixes.

## References

- Governance: `.github/copilot-instructions.md`
- Prompts: `.github/prompts/`
- Docs: `docs/vision.md`, `docs/semantic-project-model.md`, `docs/semantic-collaboration-model.md`, `docs/glossary.md`