description: Generate a minimal, self-describing Semantic Module scaffold within a parent cluster.
mode: instructions
---

# Purpose
Create a new Semantic Module that is self-describing and safe to evolve. Meaning (docs and contract) precedes mechanics (code). Module may contain one level of subdirectories for organization (e.g., /docs/, /scripts/) but no deeper nesting.

> Metadata
- id: scaffold-semantic-module
- name: Scaffold Semantic Module
- scope: module
- owners: ["@dkuwcreator"]
- version: 1.0.0
- last-updated: 2025-11-06

Inputs
- moduleName (string, required): New module name in kebab-case or snake_case
- parentClusterPath (path, required): Relative path to the target cluster directory (e.g., cluster-auth/)
- language (string, required): Primary implementation language/runtime (e.g., python, typescript)
- owners (array<string>, optional): Handles of module stewards
- shortDescription (string, optional): One-line module purpose
- initialCapabilities (array<string>, optional): Capabilities the module will provide
- invariants (array<string>, optional): Behavioral guarantees to enforce
- validationTests (array<string>, optional): Initial tests to validate invariants (e.g., test_module.py::test_happy_path)

Outputs
- proposedFileTree (markdown): Tree view of files to add
- proposedFiles (object): Map of filename -> full file content
- diff (patch): Minimal diff to create the scaffold
- commitMessage (string): Conventional Commit message

Safety
- boundedContext: true
- writePolicy: scaffold-only
- escalation: If invariants or cross-cluster dependencies are introduced, escalate to cluster steward before applying changes.

References
- governance: ../../.github/copilot-instructions.md
- vision: ../../docs/vision.md
- projectModel: ../../docs/semantic-project-model.md
- collaborationModel: ../../docs/semantic-collaboration-model.md
- glossary: ../../docs/glossary.md

# Inputs
Validate required parameters before proceeding.

# Expected outputs (contract)
- proposedFileTree: concise tree
- proposedFiles: about.md, semantic-instructions.md, a placeholder source file, and a starter test
- diff: minimal patch
- commitMessage: `docs(module): scaffold ${moduleName}`

# Safety and constraints
- Bounded context: Only operate within `{parentClusterPath}/{moduleName}/`. May include one level of subdirectories.
- Minimal diffs: Do not refactor existing modules.
- Stewardship: Include `owners` in module docs; recommend ADR if introducing novel capabilities.

# Steps (Semantic Evolution Loop)
1. Perception
   - Inspect parent cluster for naming conventions and language toolchain.
   - Confirm the module does not already exist.
2. Reasoning
   - Derive minimal files needed to express purpose and contract.
   - Map `invariants` to initial `validationTests`.
3. Action (produce proposal only)
   - Output file tree and full file contents without writing them.
   - Provide a single minimal patch.
4. Reflection
   - Check that docs clearly express intent, inputs/outputs, invariants, and validation.
   - Ensure glossary terms are used for domain language.
5. Verification
   - Include a small test that asserts at least one invariant (even as a pending/skipped test if necessary).
6. Evolution
   - Note follow-ups (e.g., implement real logic, extend tests) and any escalation needs.

# File templates (fill with provided inputs)

## about.md (template)
```markdown
# ${moduleName}

Purpose: ${shortDescription}

Capabilities:
${initialCapabilities.map(c => "- " + c).join("\n") || "- TBA"}

Ownership: ${owners && owners.length ? owners.join(", ") : "TBA"}

Related:
- Parent cluster: ${parentClusterPath}
- Glossary: ../docs/glossary.md
```

## semantic-instructions.md (template)
```markdown
---
scope: module
id: ${moduleName}
name: ${moduleName}
owners: ${owners && owners.length ? JSON.stringify(owners) : "[\"TBA\"]"}
contract:
  invariants:
${(invariants||[]).map(i=>"    - \""+i+"\"").join("\n") || "    - \"Define invariants\""}
validation:
  tests:
${(validationTests||[]).map(t=>"    - \""+t+"\" ").join("\n") || "    - \"Add initial tests\""}
change_policy:
  allowed_changes: ["scaffold", "refactor-safe", "bugfix"]
  escalation: "If invariants change, escalate to cluster steward"
---

Instructions for agents:
- Operate within this module directory. May include one level of subdirectories for organization.
- Keep changes minimal and update this file when contracts or interfaces change.
- Ensure tests reflect each invariant.
```

## Source file placeholder
- For `language=python`: create `${moduleName}.py` with a minimal function and docstring linking to invariants.
- For `language=typescript`: create `index.ts` with a minimal exported function and TODOs.

## Test file placeholder
- For `language=python`: `test_${moduleName}.py` with a basic test referencing one invariant (can be `xfail`/`skip` until implemented).
- For `language=typescript`: `test_${moduleName}.test.ts` with a basic test.

# Commit message
`docs(module): scaffold ${moduleName}`
