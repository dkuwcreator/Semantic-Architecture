# Semantic Reports Folder

Monthly or on-demand aggregated outputs of the Semantic Evolution Loop.

- Each report lives in a date-stamped folder: `data/semantic-reports/YYYY-MM-DD/`
- Typical files:
  - `summary.md` — narrative summary for humans (risks, hotspots, actions)
  - `kpis.json` — KPI snapshot (includes `schemaVersion` and `generatedBy`)
  - `drift_catalog.json` — unresolved drift by module/cluster
  - `reflection_index.json` — coverage and latency aggregates
  - `graph_delta.json` — semantic graph changes (nodes/edges/attributes)
- Optional: `attachments/` for plots or exports.

Security & provenance:

- Reports may contain internal context; treat as internal artifacts.
- Ensure emitters set `schemaVersion` and `generatedBy` consistently with metrics.
