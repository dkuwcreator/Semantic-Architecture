# 🧠 Semantic Project Model

**Version:** 2.0
**Last Updated:** 2025-11-06
**Author:** [Your Team or Organization]
**Purpose:** Define the structure, semantics, and collaboration model for AI-cooperative software development.

---

## 1. Introduction

The **Semantic Project Model** defines how larger software systems can be structured into **cognitively manageable, self-describing units** that support both **human** and **AI-assisted** development.

Instead of organizing code purely by technical layers or deployment boundaries, this model organizes it by **meaning and context** — creating units that are *understandable, modifiable, and verifiable* in isolation.

The model enables:

* AI agents to reason safely about localized code changes.
* Developers to work within small, well-bounded contexts.
* Projects to scale naturally without losing semantic clarity.

**Note:** This document defines the *structural* aspects of the Semantic Architecture. For behavioral aspects, collaboration protocols, and tooling integration, see the companion [Semantic Collaboration Model](semantic-collaboration-model.md).

---

## 2. Design Philosophy

Traditional architectures optimize for *runtime behavior* (deployability, scalability).
The **Semantic Project Model** optimizes for *cognitive behavior* — how humans and AI agents understand, modify, and evolve codebases.

This model assumes that:

* **Understanding precedes correctness.**
* **Documentation and code are inseparable parts of meaning.**
* **Local reasoning** is safer and faster than global reasoning.

By ensuring that every piece of the system — from a project to its smallest unit — is *self-describing* and *contextually complete*, AI agents can act as intelligent collaborators, not just code generators.

---

## 3. Hierarchical Overview

The Semantic Project Model defines three conceptual layers:

| Level                | Purpose                                               | Scope                  | Primary Documentation                       |
| -------------------- | ----------------------------------------------------- | ---------------------- | ------------------------------------------- |
| **Project**          | The complete software system or application           | Repository root        | `about.md`, `semantic-instructions.md`      |
| **Semantic Cluster** | A cohesive grouping of related functionality          | Subdomain or subsystem | `about.md`, `semantic-instructions.md`      |
| **Semantic Module**  | The smallest, self-contained unit of code and meaning | File set               | `about.md`, `semantic-instructions.md`      |

Each layer is a **cognitive boundary** — a distinct level at which reasoning, modification, and validation can occur.

### Visual Representation

```
┌─────────────────────────────────────────────────────────┐
│                   SEMANTIC PROJECT                      │
│                  (Repository Root)                      │
│   • about.md                                            │
│   • semantic-instructions.md                            │
│                                                         │
│   ┌──────────────────────┐   ┌──────────────────────┐  │
│   │  SEMANTIC CLUSTER    │   │  SEMANTIC CLUSTER    │  │
│   │  (Domain/Subsystem)  │   │  (Domain/Subsystem)  │  │
│   │  • about.md          │   │  • about.md          │  │
│   │  • semantic-inst...  │   │  • semantic-inst...  │  │
│   │                      │   │                      │  │
│   │  ┌──────────────┐    │   │  ┌──────────────┐    │  │
│   │  │   MODULE     │    │   │  │   MODULE     │    │  │
│   │  │  • code      │    │   │  │  • code      │    │  │
│   │  │  • about.md  │    │   │  │  • about.md  │    │  │
│   │  │  • sem-inst  │    │   │  │  • sem-inst  │    │  │
│   │  │  • tests     │    │   │  │  • tests     │    │  │
│   │  └──────────────┘    │   │  └──────────────┘    │  │
│   │                      │   │                      │  │
│   │  ┌──────────────┐    │   │  ┌──────────────┐    │  │
│   │  │   MODULE     │    │   │  │   MODULE     │    │  │
│   │  └──────────────┘    │   │  └──────────────┘    │  │
│   └──────────────────────┘   └──────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

This hierarchical structure mirrors cognitive scaling — from system-wide understanding (Project) to domain expertise (Cluster) to focused implementation (Module).

---

## 4. Projects

### Definition

A **Project** is a top-level collection of related functionality that delivers a complete software system, service, or product.
It is typically represented by a repository.

### Characteristics

* Represents an independently maintainable deliverable.
* Contains multiple **Semantic Clusters**.
* Provides a system-level `semantic-instructions.md` to define goals, interactions, and external interfaces.
* May include configuration, shared resources, or deployment artifacts.

### Example Structure

```txt
project-user-service/
├── about.md
├── semantic-instructions.md
├── cluster-auth/
│   ├── about.md
│   ├── semantic-instructions.md
│   ├── jwt_tools.py
│   ├── token_validator.py
│   └── test_auth.py
├── cluster-storage/
│   ├── about.md
│   ├── semantic-instructions.md
│   ├── blob_manager.py
│   ├── cleanup_scheduler.py
│   └── test_storage.py
└── project_config.yaml
```

---

## 5. Semantic Clusters

### Definition

A **Semantic Cluster** groups multiple **Semantic Modules** that together deliver a coherent domain capability or subsystem (e.g., *authentication*, *data storage*, *reporting*).

### Characteristics

* Represents a **bounded domain** within a project.
* Contains multiple Semantic Modules and optional shared resources.
* Provides its own `semantic-instructions.md` describing:

  * The cluster’s purpose.
  * Relationships between modules.
  * External dependencies or APIs.
* Can be developed, tested, and reasoned about independently.

### Example

```
cluster-auth/
├── about.md
├── semantic-instructions.md
├── jwt_tools.py
├── token_validator.py
├── key_cache.py
└── test_auth.py
```

### Recommended Practices

* Keep clusters **focused** — one domain or capability per cluster.
* Use the cluster-level agent instructions to describe *coordination logic* between modules.
* Maintain local test coverage that verifies interactions between contained modules.

---

## 6. Semantic Modules

### Definition

A **Semantic Module** is the smallest self-contained, semantically complete unit.
It encapsulates **code, documentation, tests, and AI guidance** in one context.

### Characteristics

* Represents one clear concept, function, or feature.
* Must include:

  * `about.md` — human-readable purpose and usage (must be at module root).
  * `semantic-instructions.md` — AI-readable structure and behavioral contract (must be at module root).
* May include additional scripts, configuration, or metadata.
* May contain one level of subdirectories (e.g., `/module/docs/`, `/module/scripts/`) but no deeper nesting is permitted.
* All files within a module and its immediate subfolders must belong to the same semantic scope.
* Should remain *small enough* that a human or AI agent can fully understand and reason about it in isolation.

### Cognitive Scope Guideline

> A Semantic Module should fit within one mental or computational "window" of comprehension.
> When it grows too complex to be understood without cross-referencing external files or contexts, it should be split into multiple smaller modules.

---

## 7. Documentation Roles

| File                       | Purpose                                                                                              | Target Audience               |
| -------------------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------- |
| `about.md`                 | Human-facing overview, usage examples, context                                                       | Developers, reviewers         |
| `semantic-instructions.md` | Machine-oriented guide describing purpose, inputs, outputs, modification rules, and validation steps | AI agents, automation systems |

Both files are **semantic anchors** — they ensure that knowledge remains co-located with the implementation.

### `semantic-instructions.md` Format

Each `semantic-instructions.md` file should start with **YAML front matter** to declare scope and semantic metadata:

```markdown
---
scope: module           # project | cluster | module
id: jwt-tools
name: JWT Tools
owners: ["@derk"]
contract:
  invariants:
    - "Reject expired tokens"
    - "Support RSA key rotation"
validation:
  tests: ["test_jwt_tools.py::test_rotation"]
change_policy:
  allowed_changes: ["bugfix", "refactor-safe"]
  escalation: "If invariants change, escalate to cluster"
---
```

Followed by detailed instructions for AI agents.

**Schema Fields:**

* **scope**: Level of the semantic unit (`project`, `cluster`, or `module`)
* **id**: Unique identifier within the parent scope
* **name**: Human-readable display name
* **owners**: List of semantic stewards responsible for this unit (see [Semantic Collaboration Model](semantic-collaboration-model.md#semantic-ownership) for details)
* **reviewers**: Optional list of additional reviewers or validation agents
* **contract**: Semantic guarantees and invariants
* **validation**: Test references and validation rules
* **change_policy**: Guidelines for safe modifications and escalation procedures

The `owners` field establishes **Semantic Stewardship** — clear accountability for maintaining the meaning and integrity of each component.

This front matter enables:

* **Schema validation**: Ensure all required fields are present
* **CI checks**: Automate validation of semantic contracts
* **Tooling integration**: Parse and understand module boundaries programmatically
* **Change impact analysis**: Track when invariants or contracts are modified

---

## 8. AI Collaboration Model

The Semantic Project Model is designed for **multi-scale AI reasoning**:

| AI Action Scope                                           | Target Layer     | Agent Context                                                          |
| --------------------------------------------------------- | ---------------- | ---------------------------------------------------------------------- |
| **Local optimization** (bug fix, refactor, feature tweak) | Semantic Module  | Operates within a single module using its documentation and tests.     |
| **Domain evolution** (e.g., add new capability)           | Semantic Cluster | Considers interactions between multiple modules within one domain.     |
| **Architectural change** (e.g., integrate new subsystem)  | Project          | Understands and modifies cluster relationships at the project level.   |

Each level provides its own contextual envelope — ensuring safe and bounded reasoning.
Agents can perform modifications proportionate to their level of understanding without overstepping contextual boundaries.

**For detailed collaboration protocols, agent roles, and workflows, see the [Semantic Collaboration Model](semantic-collaboration-model.md).**

---

## 8.1 Semantic Tooling Integration

The YAML front matter in `semantic-instructions.md` serves as the foundation for powerful semantic tooling:

### Semantic Graph Construction

The metadata enables automatic construction of a project-wide **Semantic Graph**:

* **Nodes**: Semantic Modules (identified by `scope` and `id`)
* **Edges**: Dependencies extracted from `contract` and cross-references
* **Attributes**: Owners, invariants, validation rules

This graph enables:
- Visual navigation of the codebase
- Dependency impact analysis
- Automated change validation
- AI agent path planning

### Semantic Validation Tools

Automated validators can verify:
- All required YAML fields are present and correctly formatted
- Referenced tests exist and pass
- Declared invariants align with implementation
- Ownership assignments are valid
- Cross-module references resolve correctly

### Continuous Integration

The schema integrates naturally with CI/CD pipelines:

```yaml
# Example CI check
- name: Validate Semantic Contracts
  run: semantic-check --validate-all
  
- name: Verify Ownership
  run: semantic-check --verify-owners
  
- name: Check Semantic Drift
  run: semantic-diff HEAD~1 HEAD
```

### IDE and Editor Integration

The structured metadata enables:
- Context-aware navigation (jump to module by semantic ID)
- Inline display of ownership and contracts
- Validation warnings for drift or policy violations
- AI assistant scoping based on semantic boundaries

**See [Semantic Collaboration Model](semantic-collaboration-model.md#semantic-tooling-principles) for detailed tooling specifications.**

---

## 9. Cognitive Principles

The Semantic Project Model is grounded in **cognitive load theory** and **context locality**:

| Principle                  | Description                                                             |
| -------------------------- | ----------------------------------------------------------------------- |
| **Bounded Contexts**       | Each layer defines a manageable reasoning scope.                        |
| **Context Co-Location**    | Code, tests, and documentation live together, reducing lookup overhead. |
| **Progressive Disclosure** | Higher layers reveal more context only when needed.                     |
| **Semantic Transparency**  | Every unit expresses not just what it does, but what it *means*.        |

These principles make large codebases more tractable for both human comprehension and AI-based maintenance.

---

## 10. Benefits

| Category                   | Benefit                                                           |
| -------------------------- | ----------------------------------------------------------------- |
| **Scalability**            | Projects can grow organically while preserving clarity.           |
| **AI Collaboration**       | Agents can reason safely at appropriate levels of abstraction.    |
| **Human Comprehension**    | Each layer stays cognitively manageable.                          |
| **Documentation Fidelity** | Meaning and implementation remain synchronized.                   |
| **Composable Design**      | Modules and clusters can be reused or rearranged across projects. |

---

## 11.5 Related Documents

This document is part of the Semantic Architecture framework:

### [Vision: Semantic Architecture](vision.md)
**Why:** Articulates the philosophical foundation and long-term vision. Explains the motivation behind the Semantic Architecture and its role in human-AI collaboration.

**Key Topics:**
- The problem with traditional codebases
- Knowledge Ecosystems and cognitive scalability
- Semantic Stewardship
- The Semantic Evolution Loop
- Visual overview of the complete system

### [Semantic Collaboration Model](semantic-collaboration-model.md)
**How:** Defines behavioral patterns, workflows, and tooling for operating within the Semantic Project Model.

**Key Topics:**
- Semantic Ownership and Living Knowledge Cells
- AI agent roles (Module, Cluster, Project Agents)
- Collaboration protocols and the Semantic Evolution Loop
- Semantic Validation, Semantic Graph, and Semantic Memory
- Semantic Maintenance Agents and self-healing systems

### [Glossary](glossary.md)
**Reference:** Centralized definitions of all terms and concepts.

---

## 11. Summary

The **Semantic Project Model** defines a cognitive architecture for modern, AI-cooperative software systems.
It replaces traditional “code hierarchies” with **semantic hierarchies** that mirror how understanding naturally scales — from precise, local meaning to broad, system-wide purpose.

| Layer                | Scope                       | Primary Purpose                            |
| -------------------- | --------------------------- | ------------------------------------------ |
| **Project**          | Whole application           | Integrate and expose external capabilities |
| **Semantic Cluster** | Domain or subsystem         | Organize related functionality             |
| **Semantic Module**  | Minimal self-contained unit | Define atomic, interpretable behavior      |

By adopting this model, teams create ecosystems of **intelligible, modular, and self-describing components** — where humans and AI collaborate within shared semantic boundaries.
