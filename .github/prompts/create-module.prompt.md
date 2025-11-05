---
title: Create Semantic Module
description: Scaffold a new semantic module with proper documentation structure
---

# Create a New Semantic Module

Please create a new semantic module with the following structure:

## Module Name
[Provide the module name here]

## Cluster (optional)
[Provide cluster name if this module belongs to a cluster]

## Required Files

1. **about.md** - Human-readable documentation containing:
   - Module purpose and responsibility
   - Key concepts and terminology
   - Usage examples
   - Input/output contracts
   - Key invariants

2. **semantic-instructions.md** - AI-facing instructions with:
   - YAML frontmatter with scope, id, name, owners
   - Purpose statement
   - Behavioral contracts
   - Invariants to maintain
   - Validation rules
   - Allowed changes and escalation policy

## Template Structure

```
[module-name]/
├── about.md
└── semantic-instructions.md
```

Please ensure:
- The documentation is clear and follows the Semantic Architecture principles
- Both files are synchronized in their descriptions
- Boundaries and invariants are clearly defined
- The module is small enough to be fully understood by one person or agent
