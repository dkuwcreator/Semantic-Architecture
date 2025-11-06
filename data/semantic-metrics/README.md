# Semantic Metrics Folder

This folder stores machine-generated metrics for the Semantic Evolution Loop.

- Daily metrics: `data/semantic-metrics/daily/YYYY-MM-DD.json`
- Monthly rollups: `data/semantic-metrics/monthly/YYYY-MM.json`

All metrics JSON files MUST contain the following fields:

- `schemaVersion` (string) — metrics schema version; bump on breaking schema changes or SSI-weight tuning.
- `generatedBy` (string) — emitter identifier (e.g., `semantic-evolution-ci@YYYY-MM-DD`).
- `timestamp` (ISO8601), `window` (`daily`|`monthly`), `totals`, `kpis`.
- Optional: `cluster_breakdown`, `alerts` arrays.

KPIs (units in parentheses):

- `drift_rate` (ratio 0..1)
- `validation_success_rate` (ratio 0..1)
- `reflection_coverage` (ratio 0..1)
- `reflection_latency` (days)
- `steward_response_time_days` (days)
- `ssi` (0..100)

Example (daily):

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
  }
}
```
