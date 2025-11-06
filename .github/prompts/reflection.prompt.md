# Reflection Prompt — Semantic Evolution Loop

Use this prompt to generate a concise reflection and memory entry after Action.
Keep scope bounded (module/cluster). Never self-merge; route through stewards.

---
YAML Front Matter (required)
---
schemaVersion: 1.0
scope: <module|cluster>
id: <semantic-id>
date: <ISO-8601>
summary: <short-intent-summary>
changedContracts:
  # List specific contract/interface changes that affect semantics.
  # Examples:
  # - name: verify_token
  #   change: "added parameter allow_rotation: bool = false"
  #   invariantImpact: "Support RSA key rotation"
  # - name: semantic-instructions.md
  #   change: "updated invariants to include rotation support"
  - 
invariantsTouched:
  - 
adrLinks:
  - 
owners:
  - 
reviewChecklist:
  intentStatedBeforeExecution: true
  testsUpdatedOrAdded: true
  invariantsReviewed: true
  ownersNotified: true
---

## Reflection
- Intent: <why this change exists>
- Scope: <module or cluster>
- Summary of diffs: <1-3 bullet points>
- Validation notes: <tests/validation outcomes>
- Risk/impact: <low|medium|high> with rationale

## Next Steps
- ADR updates or proposals
- Follow-up tasks
- Steward decision needed?
