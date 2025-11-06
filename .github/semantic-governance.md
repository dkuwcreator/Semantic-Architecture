---
description: Phase 7 Governance Charter for the Semantic Architecture
scope: project
id: governance-charter
version: 1.0.0
owners: ["@dkuwcreator"]
last-updated: 2025-11-06
links:
  - root-governance: ./.github/copilot-instructions.md
  - vision: ../docs/vision.md
  - project-model: ../docs/semantic-project-model.md
  - collaboration-model: ../docs/semantic-collaboration-model.md
  - glossary: ../docs/glossary.md
---

# Semantic Governance Charter — Phase 7

Purpose: Institutionalize long-term stewardship to preserve semantic integrity, accountability, and continuous improvement across the Semantic Evolution Loop after Phase 6 automation. This charter maps roles to semantic layers, defines cadences and KPIs, and specifies decision and escalation policies so the system remains intelligible and self-sustaining over time.

## Alignment & scope

- Aligned with the Semantic Architecture’s three layers: Project → Cluster → Module.
- Implements the Perception → Reasoning → Action → Reflection → Verification → Evolution loop operationally.
- Nearest-context precedence applies (Module > Cluster > Project) unless an ADR declares a broader exception.

## Roles and responsibilities (bounded to layers)

### Project Stewards (architectural oversight)

- Scope: Project-wide coherence, cross-cluster contracts, and architecture.
- Duties:
  - Approve cross-cluster ADRs and major semantic contract changes.
  - Own quarterly Semantic Graph health checks and System Stability Index (SSI).
  - Triage `requires-steward(project)` within 3 business days.
- Success: SSI ≥ 85 sustained; no unresolved project-level drift > 2 cycles.

### Cluster Stewards (domain guardians)

- Scope: One cluster’s semantic coherence across modules.
- Duties:
  - Resolve cluster-level drift; maintain cluster docs and invariants.
  - Run monthly evolution reviews; approve cluster ADRs.
  - Triage `requires-steward(cluster:<name>)` within 2 business days.
- Success: Cluster drift ≤ project median; validation ≥ 98%.

### Module Stewards (local maintainers)

- Scope: Single module (Knowledge Cell).
- Duties:
  - Keep `about.md` and `semantic-instructions.md` in sync; ensure reflection on changes.
  - Maintain local tests; close unresolved drift within one cycle.
  - Triage `requires-steward(module:<id>)` within 1 business day.
- Success: 0 unresolved drift > 1 cycle; reflection coverage ≥ 90%.

### AI Maintenance Agents (continuous validators)

- Scope: Project-wide scanning, validation, graph updates.
- Duties:
  - Export metrics to `data/semantic-metrics/`; create daily/rolling aggregates.
  - Open issues on drift/violations with correct labels and evidence.
  - Post reflection summaries linked to PRs/issues.
- Success: Accurate metrics, timely issues, minimal false positives.

## Cadence & rituals

- Weekly (30–45m) Semantic Review: review drift, failed validations, reflection gaps, SSI delta. Output: labeled issues with owners/dates.
- Monthly (60–90m) Evolution Report: trend KPIs by cluster; publish to `data/semantic-reports/YYYY-MM-DD/`.
- Quarterly (120m) ADR Audit + Graph Health: reconcile ADRs to contracts; identify gravity hotspots; plan refactors/ownership rotations.

## KPIs (definitions, targets, thresholds)

- Drift rate: unresolved_drift_modules / total_modules. Target ≤ 5% weekly. Alert ≥ 10% or +5pp WoW.
- Validation success rate: passed_tests / total_tests. Target ≥ 99%. Alert < 98%.
- Reflection coverage: changes_with_reflection / total_changes. Target ≥ 90%. Alert < 80%.
- Reflection latency (days): mean days from merge to reflection log attached. Target ≤ 1.0; Alert > 2.0.
- Steward response time (days): mean days from `requires-steward(*)` to first steward response. Targets: Module ≤ 1, Cluster ≤ 2, Project ≤ 3.
- System Stability Index (SSI, 0–100):

  ```text
  SSI = round(100 * (0.30*(1 - drift_rate) + 0.40*validation_success_rate + 0.20*reflection_coverage + 0.10*min(1, 3/response_time_days)))
  ```

  - Weights are tunable. Steward council may adjust via ADR; record change in this charter and bump metrics `schemaVersion`.

## Decision and change policy

- ADR required when: changing cluster/project semantic contracts; cross-cluster boundaries shift; SSI < 80 for 2 consecutive months.
- Review thresholds:
  - Minor (module-only, backward compatible): Cluster steward approval.
  - Moderate (cluster-wide or additive ABI): Cluster + Project steward approval.
  - Major (breaking contracts / cross-cluster refactors): ADR + Project steward approval.
- Version bump semantics:
  - Breaking invariant/behavior → major.
  - Additive capability / new module → minor.
  - Docs/tests/prompt tuning (no behavior change) → patch.
- Ownership rotation & succession:
  - Cluster-level rotation quarterly; module rotation optional monthly.
  - Each steward names a deputy; deputy auto-escalates if SLAs breach or OOO.
  - Handover includes open issues, drift list, active ADRs, KPI snapshot.

## Communication, labels, and escalation

- Labels: `semantic-review`, `requires-steward(project|cluster:<name>|module:<id>)`, `drift-detected`, `adr-required`, `evolution-report`, `governance`, plus `cluster:<name>`, `module:<id>` for routing.
- Escalation path: Module → Cluster (≤ 48h) → Project (≤ 72h or on severity/threshold breach).
- Ownership hygiene: use CODEOWNERS per cluster/module; deputies listed in `docs/steward-roles.md`. PRs auto-request reviews from stewards.

## Integration with automation (Phase 6 → Phase 7)

- Sources: `scripts/semantic_validator.py`, `scripts/semantic_drift_scanner.py`, `scripts/semantic_graph.py`, `scripts/ci_check.ps1`.
- Writeouts:
  - Daily JSON → `data/semantic-metrics/daily/YYYY-MM-DD.json`.
  - Monthly rollup → `data/semantic-metrics/monthly/YYYY-MM.json`.
  - Reports → `data/semantic-reports/YYYY-MM-DD/` (summary.md, kpis.json, drift_catalog.json, reflection_index.json, graph_delta.json).
- Required JSON fields (all metrics files):
  - `schemaVersion` (string), `generatedBy` (string), `timestamp`, `window`, `totals`, `kpis`, optional `cluster_breakdown`, `alerts`.
  - KPIs include: `drift_rate`, `validation_success_rate`, `reflection_coverage`, `reflection_latency` (days), `steward_response_time_days`, `ssi`.
- Reflection logs: CI appends entries linked to PRs; coverage and latency computed from these logs.

## Security & secrets (notifications)

- CI notifications (Teams/Slack) use organization/repository GitHub Actions secrets.
- Store webhooks as secrets (examples): `TEAMS_WEBHOOK_URL`, `SLACK_WEBHOOK_URL`.
- Do not commit or echo secret values. Consume only within workflows; restrict to necessary jobs; rotate on ownership changes.

## Continuous improvement

- Monthly retrospective: review KPIs vs targets, false positives, steward workload; decide prompt tuning/agent retraining/test hardening.
- Prompt/agent changes: record deltas; A/B test ≤ 2 cycles; adopt if SSI and drift trends improve.
- Charter updates: amend this file for policy changes; link to ADRs and relevant monthly reports; update `version` as needed.

## Directory layout (artifacts)

```text
data/
  semantic-metrics/
    daily/
    monthly/
  semantic-reports/
    YYYY-MM-DD/
  semantic-audits/            # optional, quarterly artifacts
```

## Example metrics JSON (daily)

```json
{
  "schemaVersion": "1.0",
  "generatedBy": "semantic-evolution-ci@2025-11-06",
  "timestamp": "2025-11-06T23:59:59Z",
  "window": "daily",
  "totals": { "modules": 128, "tests": 1742, "changes": 29 },
  "kpis": {
    "drift_rate": 0.035,
    "validation_success_rate": 0.992,
    "reflection_coverage": 0.914,
    "reflection_latency": 0.4,
    "steward_response_time_days": 0.8,
    "ssi": 88
  },
  "cluster_breakdown": {
    "auth": { "drift_rate": 0.02, "validation_success_rate": 0.995, "reflection_coverage": 0.93, "ssi": 91 }
  },
  "alerts": [
    { "type": "drift", "severity": "medium", "message": "3 modules with unresolved drift", "related": { "cluster": "storage" } }
  ]
}
```
