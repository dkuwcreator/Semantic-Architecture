---
scope: project
id: semantic-architecture
name: Semantic Architecture
owners: ["@dkuwcreator"]
contract:
  invariants:
    - "Maintain clarity of documentation structure"
    - "Ensure human-facing and AI-facing documentation remain synchronized"
    - "Preserve the three-layer hierarchy (Project, Cluster, Module)"
validation:
  tests: []
change_policy:
  allowed_changes: ["documentation", "structure", "examples"]
  escalation: "Major architectural changes require community discussion"
---

# Semantic Architecture - AI Instructions

## Purpose

This project defines the **Semantic Architecture** framework — a vision and methodology for organizing software systems to enable effective human–AI collaboration through semantic clarity and bounded contexts.

## Structure

The project consists of:

- **Documentation files**: `about.md`, `VISION.md`, and model descriptions
- **No executable code**: This is a documentation-only project defining architectural patterns

## Scope

This project level encompasses the entire semantic architecture vision and methodology. The framework defines:

1. **Project Layer**: Complete software systems
2. **Semantic Cluster Layer**: Related capabilities or domains  
3. **Semantic Module Layer**: Smallest self-contained units

## Key Principles

- **Bounded Context**: Keep reasoning localized and safe
- **Local Knowledge**: Every module contains all needed information
- **Meaning First**: Documentation and code are equal partners
- **Self-Maintenance**: Systems detect and repair drift automatically
- **Shared Understanding**: Humans and AI work from the same semantic map

## Documentation Standards

### Human-Facing Documentation (`about.md`)

- Clear, minimal, and developer-friendly
- Used at all levels: Project, Cluster, Module
- Provides overview, context, and usage examples

### AI-Facing Instructions (`semantic-instructions.md`)

- Consistent, automation-friendly structure
- Includes YAML front matter with scope and metadata
- Used at all levels: Project, Cluster, Module
- Contains behavioral contracts, invariants, and validation rules

## Modification Rules

When modifying this project:

1. **Consistency First**: Ensure all documentation files reflect the same conventions
2. **Update All Levels**: If changing naming or structure, update all example hierarchies
3. **Preserve Intent**: Changes should enhance clarity, not obscure meaning
4. **Synchronize Documentation**: Keep about.md and semantic-instructions.md aligned

## Invariants to Maintain

- All documentation must use consistent naming conventions
- Examples must accurately reflect the defined structure
- The three-layer hierarchy must remain clear and distinct
- Human and AI documentation must be clearly separated and labeled

## Integration Points

This is a standalone documentation project with no external dependencies or integrations. It serves as a reference and guide for implementing semantic architecture in actual software projects.

## Future Evolution

This framework is designed to evolve based on:

- Real-world implementation experiences
- Community feedback and contributions
- Advances in AI collaboration capabilities
- Lessons learned from semantic architecture adoption
