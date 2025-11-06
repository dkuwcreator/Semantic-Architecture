---
title: Steward Roles, Rotations, and Checklists
scope: project
id: steward-roles
version: 1.0.0
last-updated: 2025-11-06
links:
  - charter: ../.github/semantic-governance.md
  - project-model: ./semantic-project-model.md
  - collaboration-model: ./semantic-collaboration-model.md
  - glossary: ./glossary.md
---

## Steward Roles, Rotations, and Checklists

This document operationalizes the Phase 7 governance charter with detailed role definitions, rotations, SLAs, and checklists mapped to the three semantic layers.

## Role overview

### Project Steward

- Scope: Project layer (architecture, cross-cluster contracts, SSI).
- Primary duties:
  - Approve cross-cluster ADRs and major semantic contract changes.
  - Oversee quarterly Semantic Graph health checks and SSI trends.
  - Maintain `.github/semantic-governance.md` and ensure policy links to ADRs/reports.
- SLAs: Triage `requires-steward(project)` ≤ 3 business days.
- Deputy: Required. Deputies act on SLA breaches or OOO.

### Cluster Steward

- Scope: A single cluster (domain coherence across modules).
- Primary duties:
  - Run monthly evolution reviews; coordinate inter-module invariants/tests.
  - Resolve cluster-level drift; propose ADRs for boundary shifts.
  - Keep cluster docs current; curate cluster-specific labels.
- SLAs: Triage `requires-steward(cluster:<name>)` ≤ 2 business days.
- Deputy: Recommended for larger clusters.

### Module Steward

- Scope: One module (Knowledge Cell).
- Primary duties:
  - Keep `about.md` and `semantic-instructions.md` synchronized with code.
  - Ensure tests validate declared invariants; fix drift within one cycle.
  - Attach reflection logs to changes; maintain reflection coverage and latency.
- SLAs: Triage `requires-steward(module:<id>)` ≤ 1 business day.
- Deputy: Optional; recommended for critical modules.

### AI Maintenance Agent

- Scope: Project-wide continuous perception and verification.
- Primary duties:
  - Export metrics to `data/semantic-metrics/` with `schemaVersion` and `generatedBy`.
  - Open/label issues for drift and validation failures; include evidence artifacts.
  - Post reflection summaries linked to PRs/issues; compute reflection coverage/latency.
- SLAs: Post daily metrics; open issues within the same cycle when thresholds breach.

## Rotation & succession

- Rotation cadence:
  - Cluster stewards rotate quarterly; module stewards may rotate monthly in large teams.
  - Deputies are named in advance; automatic elevation on SLA breach or OOO.
- Handover checklist:
  - Review open issues and drift list; confirm owners/dates.
  - Review active ADRs and pending approvals.
  - Share KPI snapshot (cluster/module) and recent reflection trends.
  - Confirm CODEOWNERS entries and labels are accurate.

## Ownership & routing

- Use CODEOWNERS to map clusters/modules to stewards and deputies.
- Label taxonomy:
  - `requires-steward(project|cluster:<name>|module:<id>)`
  - `drift-detected`, `adr-required`, `evolution-report`, `governance`
  - Optional: `cluster:<name>`, `module:<id>` to aid automation routing.

## Checklists

### Weekly (all stewards)

1. Review drift list and validation failures for your scope.
2. Verify reflection coverage and outliers in reflection latency.
3. Assign owners/dates; ensure labels are correct; escalate as needed.

### Monthly (cluster + project)

1. Read `data/semantic-reports/YYYY-MM-DD/summary.md` and KPIs.
2. Identify hotspots (high gravity, recurring drift, low reflection).
3. Propose ADRs or refactors; tune prompts/agents if warranted.

### Quarterly (project)

1. Audit ADRs vs actual contracts/invariants.
2. Validate Semantic Graph congruence and gravity hotspots.
3. Review SSI trend; confirm weight tuning still appropriate.
4. Confirm rotations and deputies; update charter if systemic issues persist.

## Security & secrets

- Webhook secrets for Teams/Slack are stored as GitHub Actions secrets (e.g., `TEAMS_WEBHOOK_URL`, `SLACK_WEBHOOK_URL`).
- Never commit or echo secret values; use in workflows only.
- Rotate secrets during ownership changes or suspected exposure.

## Metrics fields (required in all metrics JSON)

- `schemaVersion` (string) — metrics schema version (bump on breaking changes or SSI-weight changes).
- `generatedBy` (string) — emitter identifier (e.g., `semantic-evolution-ci@YYYY-MM-DD`).
- `timestamp` (ISO8601), `window` (daily|monthly), `totals`, `kpis`, optional `cluster_breakdown`, `alerts`.
- KPIs include: `drift_rate`, `validation_success_rate`, `reflection_coverage`, `reflection_latency` (days), `steward_response_time_days`, `ssi`.

## Onboarding quick start

- Read the charter and this document; understand your scope and SLAs.
- Ensure CODEOWNERS and labels are correct for your area.
- Review last report in `data/semantic-reports/` and recent metrics in `data/semantic-metrics/`.
- Schedule the next cadence meeting if not already on the calendar.
