---
description: Apply explicitly approved remediation edits to spec.md, plan.md, and/or tasks.md produced by /speckit.analyze. Makes only the requested changes.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Apply a set of **explicitly approved remediation edits** (typically derived from `/speckit.analyze`) to the three core artifacts:

- `spec.md`
- `plan.md`
- `tasks.md`

This command is the **write-mode follow-up** to `/speckit.analyze` and should be run only after:

1.  `/speckit.tasks` has produced `tasks.md`, and
2.  `/speckit.analyze` has produced remediation recommendations, and
3.  the user has **explicitly approved** the remediations to apply.

## Operating Constraints

### Scope Lock (No “extra improvements”)

**EDIT ONLY WHAT IS REQUESTED** in `$ARGUMENTS`: Do **not** perform additional analysis, cleanup, refactoring, or enhancements beyond the explicitly approved remediation set. If an edit implies dependent changes (e.g., renaming a term referenced elsewhere), only apply those dependent changes if they are **explicitly included** in `$ARGUMENTS`.

**Constitution Authority**: The project constitution (`.specify/memory/constitution.md`) is **non-negotiable** within this remediation scope. If an approved remediation conflicts with a MUST principle, **do not apply it**. Report it as **BLOCKED (CRITICAL)** and instruct the user to revise the remediation or update the constitution in a separate explicit step.

### Safety & Determinism

- Prefer **minimal diffs** (smallest change that satisfies the remediation).
- Preserve existing formatting, headings, IDs, ordering, and conventions unless the remediation explicitly changes them.
- Maintain stable task IDs and phase groupings; do not renumber tasks unless explicitly directed.

### Required Approval Signal

This command MUST NOT proceed unless `$ARGUMENTS` includes an explicit approval signal:

- `APPROVED: YES` (preferred), or
- `APPROVE`, or
- `I APPROVE`

If approval is missing, abort with instructions.

## Expected Input Format (Recommended)

`$ARGUMENTS` should include:

1.  an approval signal, and
2.  a remediation list.

### Option A (Preferred): Structured YAML directives

```yaml
APPROVED: YES
APPLY:
  - id: A1
    file: spec.md
    operation: replace
    anchor: "## Functional Requirements"
    match: "The system should be fast."
    content: "The system must respond within 300ms p95 for read operations under 500 RPS."
  - id: C3
    file: tasks.md
    operation: insert_after
    anchor: "### Phase 2"
    content: |
      - [ ] T2.7 Add performance test harness for p95 latency target (maps: performance-p95-latency)
```

### Option B: Paste “Top N Remediations” in text form

Must include per-item:

- Finding/Remediation ID (e.g., A1, E2, D4)
- Target file(s)
- Exact replacement text or explicit instruction (insert/delete/replace)

If Option B is ambiguous, abort and request Option A.

## Execution Steps

### 1. Initialize Remediation Context

Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` once from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive absolute paths:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

Abort with an error message if any required file is missing (instruct the user to run missing prerequisite command).

For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'''m Groot' (or double-quote if possible: "I'm Groot").

### 2. Validate Approval + Parse Directives

- Confirm `$ARGUMENTS` contains explicit approval.
- Parse remediation directives:
    - Prefer YAML (Option A).
    - If freeform text (Option B), extract a deterministic directive list.
- If directives are incomplete or ambiguous (missing file, missing operation, missing content, missing anchor/match for replacements), **abort** and request structured YAML.

### 3. Load Constitution (Read-Only)

Load `.specify/memory/constitution.md` to validate that each remediation does not violate any MUST principles.

### 4. Progressive Artifact Loading (Minimal)

Load only the minimal context required per directive:

- For `replace`: load around `anchor` and `match` sections only.
- For `insert_after` / `insert_before`: load the target section around `anchor`.
- For `delete`: load the exact section identified by `anchor` + `match`.

Do not load unrelated sections.

### 5. Apply Remediations (Exactness Rules)

For each directive, apply changes as follows:

#### Operations

- **replace**: Replace the first exact match near the anchor. If multiple matches exist:
    - apply only if directive includes a disambiguator (e.g., additional `match_context`),
    - otherwise abort and report ambiguity.
- **insert_after / insert_before**: Insert exactly the provided content at the specified anchor.
- **delete**: Remove only the matched block or line(s) specified by the directive.

#### Guards

- If a directive would cause a constitution violation → do not apply, mark BLOCKED (CRITICAL).
- If anchor/match cannot be found → do not guess; mark FAILED (HIGH) and report.
- If applying the change would break Markdown structure (e.g., heading nesting) → adjust only insofar as needed to keep Markdown valid, and report the adjustment as part of the same directive (no extras).

### 6. Post-Edit Sanity Pass (Non-Analytical)

Perform a minimal integrity check:

- Ensure the three files still exist and are readable.
- Ensure no obvious merge artifacts were introduced (e.g., `<<<<<<<`, `=======`, `>>>>>>>`).
- Ensure directives did not introduce placeholders like `TODO`, `TKTK`, `???` unless explicitly included.

Do NOT perform cross-artifact semantic analysis (that is `/speckit.analyze`’s job).

### 7. Produce Remediation Implementation Report (No File Writes Beyond Remediations)

Output a compact Markdown report:

## Remediation Implementation Report

### Applied

| Directive ID | File | Operation | Result | Notes |
| ------------ | ---- | --------- | ------ | ----- |

### Blocked (Constitution Conflict)

(List any blocked directives and the MUST principle impacted)

### Failed / Skipped

(List any directives that could not be applied due to missing anchors, ambiguous matches, or insufficient instructions)

### Recommended Next Step

- Run `/speckit.analyze` again to confirm improvements and detect any remaining issues.

## Operating Principles

- **Do exactly what the directives say**; nothing more.
- **Do not silently reinterpret** instructions.
- **Do not broaden scope** beyond listed remediations.
- **Never modify the constitution** within this command.
- **Abort on ambiguity** rather than guessing.