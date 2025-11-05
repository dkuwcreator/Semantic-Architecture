# GitHub Copilot Instructions for Semantic Architecture

When working on this project, please follow these guidelines:

## Project Structure

This repository defines the **Semantic Architecture** framework - a methodology for organizing software systems to enable effective human-AI collaboration through semantic clarity and bounded contexts.

## Core Principles

1. **Bounded Context**: Keep reasoning localized and safe
2. **Local Knowledge**: Every module contains all needed information
3. **Meaning First**: Documentation and code are equal partners
4. **Self-Maintenance**: Systems detect and repair drift automatically
5. **Shared Understanding**: Humans and AI work from the same semantic map

## Documentation Standards

### For all documentation changes:
- Maintain consistency across all documentation files
- Ensure human-facing (`about.md`, `README.md`) and AI-facing (`semantic-instructions.md`) documentation remain synchronized
- Preserve the three-layer hierarchy: Project → Cluster → Module

### Writing Style:
- Use clear, minimal, developer-friendly language
- Include concrete examples where appropriate
- Keep explanations concise but complete

## MCP Server

This repository includes an MCP (Model Context Protocol) server in the `mcp-server/` directory that exposes the framework's documentation and tools. When modifying the MCP server:

- Ensure all resources point to valid documentation files
- Keep tool schemas in sync with actual implementation
- Test changes locally before committing

## Change Policy

- **Documentation updates**: Can be made directly
- **Structural changes**: Should be discussed with maintainers
- **Major architectural changes**: Require community discussion

## Semantic Module Structure

When creating examples or templates, ensure modules follow this structure:
```
module-name/
├── about.md                    # Human-readable documentation
└── semantic-instructions.md    # AI-facing instructions with YAML frontmatter
```

## Testing Changes

For MCP server changes:
```bash
cd mcp-server
npm install
npm run build
npm start
```

Then test with a compatible MCP client or using the VS Code configuration in `.vscode/mcp.json`.
