---
title: Validate Semantic Structure
description: Check that the repository follows Semantic Architecture principles
---

# Validate Semantic Architecture Structure

Please validate the semantic structure of this repository:

## Checks to Perform

1. **Module Structure**
   - Verify each module has `about.md` and `semantic-instructions.md`
   - Check that documentation follows the standard format
   - Ensure YAML frontmatter is present and valid in semantic-instructions.md

2. **Hierarchy**
   - Confirm the Project → Cluster → Module hierarchy is clear
   - Verify there are no deeply nested structures (should be flat)
   - Check that clusters are optional and properly organized

3. **Documentation Consistency**
   - Ensure human-facing and AI-facing docs describe the same module
   - Verify that purpose, boundaries, and invariants are consistent
   - Check that examples are accurate and up-to-date

4. **Semantic Principles**
   - Bounded context: Modules are self-contained
   - Local knowledge: All information is present in the module
   - Meaning first: Documentation is complete and clear

## Report Format

Please provide:
- List of modules found
- Any missing documentation files
- Inconsistencies or violations of principles
- Suggestions for improvement
