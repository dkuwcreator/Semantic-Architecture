---
description: "Task list for Semantic Architecture Foundation Pack"
---

# Tasks: Semantic Architecture Foundation Pack

**Input**: Design documents from `/specs/001-semantic-foundation-pack/` (`plan.md`, `spec.md`)

**Notes**:
- Repo is documentation-first; tasks focus on Markdown artifacts.
- “Tests” in `spec.md` are acceptance scenarios/manual verification; no automated tests are generated because none are requested.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Every task includes an exact file path and a per-task DoD.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Minimal folder scaffolding needed for doc artifacts

- [X] T001 Create required top-level folders `templates/`, `examples/`, `adapters/` (DoD: folders exist; no content yet)
- [X] T002 [P] Add placeholder `.gitkeep` files for empty dirs `templates/.gitkeep`, `examples/.gitkeep`, `adapters/.gitkeep` (DoD: Git tracks empty dirs)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Contribution/review guardrails that apply to all story work

**⚠️ CRITICAL**: This phase must complete before polishing/merging story work.

- [X] T003 Create contribution workflow doc in `CONTRIBUTING.md` (DoD: documents spec → plan → tasks → implement workflow; includes drift/boundary review expectations)
- [X] T004 [P] Add PR checklist in `.github/pull_request_template.md` (DoD: includes bounded context + drift-policy compliance checklist items)

**Checkpoint**: Foundation ready - user story work can proceed with review guardrails

---

## Phase 3: User Story 1 - Understand & Apply the Core Model (Priority: P1) 🎯 MVP

**Goal**: Provide a single normative core spec (tool-agnostic) and clear repository navigation

**Independent Test**: A reader can answer (from the core spec alone):
- What is Semantic Architecture?
- How do I structure my project (Project/Cluster/Module)?
- How do I prevent/resolve drift?

### Implementation for User Story 1

- [X] T005 [US1] Create normative core spec in `docs/core-spec.md` (DoD: includes MUST/SHOULD/MAY rules for Project/Cluster/Module, required artifacts, escalation model, drift definition + workflow; explicitly tool-agnostic)
- [X] T006 [US1] Update repository navigation in `README.md` (DoD: “Start here” links to core spec, templates, example, adapters; clearly labels adapters as optional/non-normative and MCP server as tooling)
- [X] T007 [P] [US1] Align terminology in `docs/semantic-project-model.md` with the core spec (DoD: no conflicting definitions; adds link back to `docs/core-spec.md` where appropriate)
- [X] T008 [P] [US1] Align terminology in `docs/semantic-collaboration-model.md` with the core spec (DoD: escalation/drift terms match; links back to `docs/core-spec.md` where appropriate)
- [X] T009 [P] [US1] Update `docs/glossary.md` for any new/renamed terms (DoD: glossary contains Project/Cluster/Module/Meaning Artifacts/Drift/Adapter entries matching core spec language)

**Checkpoint**: Core model is readable, normative, and navigable from README

---

## Phase 4: User Story 2 - Start with Templates (Priority: P2)

**Goal**: Provide reusable, tool-agnostic templates for modules and clusters

**Independent Test**: A reader can copy templates into another repo and produce a valid Module/Cluster structure without any tool-specific docs.

### Implementation for User Story 2

- [X] T010 [P] [US2] Create module README template in `templates/semantic-module/README.md` (DoD: contains required headings: Purpose/Intent, Scope, Context, Constraints, Validation, Drift checks; no tool/vendor language)
- [X] T011 [P] [US2] Create module agent instructions template in `templates/semantic-module/AGENT_INSTRUCTION.md` (DoD: contains boundaries, allowed/forbidden changes, escalation triggers, invariants, verification steps; no tool/vendor language)
- [X] T012 [P] [US2] Create cluster overview template in `templates/semantic-cluster/README.md` (DoD: includes cluster purpose, module index, boundaries, escalation guidance, drift hotspots)
- [X] T013 [US2] Cross-link templates to the normative rules in `docs/core-spec.md` (DoD: templates reference core spec for definitions; do not introduce conflicting rules)

**Checkpoint**: Templates are copy/paste usable and consistent with core spec

---

## Phase 5: User Story 3 - Learn by Example (Priority: P3)

**Goal**: Provide a tiny reference example (1 project, 1 cluster, 2–3 modules) demonstrating boundaries, required artifacts, and drift handling

**Independent Test**: Example is understandable end-to-end; each module is understandable in isolation using only its local files.

### Implementation for User Story 3

- [X] T014 [US3] Create example project overview in `examples/minimal-project/README.md` (DoD: explains layout; clearly states example is illustrative and non-normative)
- [X] T015 [US3] Create example cluster overview in `examples/minimal-project/cluster-foundation/README.md` (DoD: lists modules + responsibilities; boundaries are clear)
- [X] T016 [P] [US3] Create Module Alpha meaning artifacts in `examples/minimal-project/cluster-foundation/module-alpha/README.md` and `examples/minimal-project/cluster-foundation/module-alpha/AGENT_INSTRUCTION.md` (DoD: boundaries + escalation triggers explicit; consistent with templates)
- [X] T017 [P] [US3] Create Module Beta meaning artifacts in `examples/minimal-project/cluster-foundation/module-beta/README.md` and `examples/minimal-project/cluster-foundation/module-beta/AGENT_INSTRUCTION.md` (DoD: boundaries + escalation triggers explicit; consistent with templates)
- [X] T018 [P] [US3] Add tiny illustrative stubs for Alpha/Beta in `examples/minimal-project/cluster-foundation/module-alpha/stub.py` and `examples/minimal-project/cluster-foundation/module-beta/stub.py` (DoD: each file is intentionally tiny; header comment states “illustrative” and “non-normative”)
- [X] T019 [US3] Document drift scenario in `examples/minimal-project/DRIFT_SCENARIO.md` (DoD: includes before/after mismatch; shows detect → escalate → update steps; points to core spec drift workflow)

**Checkpoint**: Example demonstrates structure + drift handling without becoming large

---

## Phase 6: User Story 4 - Use Optional Tool Adapters (Priority: P4)

**Goal**: Provide explicitly non-normative adapter docs (Spec Kit) that do not redefine the core model

**Independent Test**: Reader can ignore adapters entirely; adapter is clearly optional and non-normative.

### Implementation for User Story 4

- [X] T020 [US4] Create Spec Kit adapter guide in `adapters/spec-kit/README.md` (DoD: clearly labeled NON-NORMATIVE; describes how Spec Kit supports workflow without changing MUST/SHOULD/MAY rules)
- [X] T021 [US4] (Optional) Add workflow example in `adapters/spec-kit/workflow.md` (DoD: includes example folder conventions/commands; reiterates non-normative status)

**Checkpoint**: Adapter accelerates workflow without leaking into core spec

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Consistency, link integrity, and drift-proofing across docs/templates/examples

- [X] T022 [P] Run terminology consistency pass across `docs/`, `templates/`, `examples/` (DoD: no contradictory definitions; normative vs non-normative labels are consistent)
- [X] T023 [P] Validate internal links in `README.md`, `docs/core-spec.md`, templates, and example READMEs (DoD: all links resolve on GitHub; no broken relative links)
- [X] T024 Ensure `kebab-case` naming conventions are used in all new example/template paths (DoD: no new dirs/files violate naming convention)

---

## Dependencies & Execution Order

### User Story Dependencies

- **US1 (P1)**: No dependencies; should be done first (MVP)
- **US2 (P2)**: Depends on US1 terminology/rules
- **US3 (P3)**: Depends on US1; benefits from US2 (templates) for consistency
- **US4 (P4)**: Depends on US1 (core rules must remain tool-agnostic)

### Suggested Completion Order (Dependency Graph)

`Phase 1 → Phase 2 → US1 → US2 → US3 → US4 → Polish`

---

## Parallel Opportunities

### Setup / Foundational

- [P] tasks: `T002`, `T004` can be done in parallel with other work once directory scaffolding exists.

### US1

- Parallelizable doc alignment: `T007`, `T008`, `T009` after `T005` exists.

### US3

- Module Alpha/Beta artifacts: `T016` and `T017` can be done in parallel.
- Code stubs: `T018` can be parallel once module folders exist.

---

## Suggested Commit Boundaries (Small, Reviewable)

- Commit A: Setup scaffolding (`T001–T002`)
- Commit B: Contribution + PR checklist (`T003–T004`)
- Commit C (MVP): Normative core spec + README navigation (`T005–T006`)
- Commit D: Terminology alignment across existing docs (`T007–T009`)
- Commit E: Templates (`T010–T013`)
- Commit F: Minimal example structure + module artifacts + stubs (`T014–T018`)
- Commit G: Drift scenario write-up (`T019`)
- Commit H: Spec Kit adapter docs (`T020–T021`)
- Commit I: Consistency/link pass (`T022–T024`)
