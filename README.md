# Semantic Architecture

**Version:** 2.0  
**Last Updated:** 2025-11-06

---

## Overview

The **Semantic Architecture** is a comprehensive framework for designing software systems that prioritize **understanding** alongside execution. It enables effective collaboration between humans and AI agents through shared context, clear boundaries, and semantic coherence.

This repository contains the complete documentation suite for the Semantic Architecture framework.

---

## 📚 Documentation Structure

The framework consists of four core documents, each serving a distinct purpose:

### 1. [Vision: Semantic Architecture](docs/vision.md)
**The "Why"** — Philosophical foundation and long-term vision

Explores the motivation behind Semantic Architecture and its role in enabling human-AI collaboration. Introduces core concepts like Knowledge Ecosystems, Semantic Stewardship, and the Semantic Evolution Loop.

**Start here if:** You want to understand the big picture and philosophy.

---

### 2. [Semantic Project Model](docs/semantic-project-model.md)
**The "What"** — Structural specifications and schema definitions

Defines the three-layer hierarchy (Project → Cluster → Module), documentation standards, YAML schema for semantic metadata, and cognitive principles.

**Start here if:** You want to implement or structure a Semantic Architecture project.

---

### 3. [Semantic Collaboration Model](docs/semantic-collaboration-model.md)
**The "How"** — Behavioral patterns and collaboration protocols

Describes how humans and AI agents work together, including agent roles, the Semantic Evolution Loop as a practical protocol, semantic tooling, and maintenance patterns.

**Start here if:** You want to understand workflows and collaboration practices.

---

### 4. [Glossary](docs/glossary.md)
**The Reference** — Centralized terminology definitions

Comprehensive reference of all terms, concepts, and patterns used across the Semantic Architecture framework.

**Start here if:** You need quick definitions or want to understand specific terminology.

---

## 🎯 Key Concepts

### Three-Layer Hierarchy

```
┌─────────────────────────────────────────────────┐
│          SEMANTIC PROJECT                       │
│  (Complete System / Repository)                 │
│                                                 │
│  ┌───────────────┐  ┌───────────────┐          │
│  │   CLUSTER     │  │   CLUSTER     │          │
│  │   (Domain)    │  │   (Domain)    │          │
│  │               │  │               │          │
│  │  ┌─────────┐  │  │  ┌─────────┐  │          │
│  │  │ MODULE  │  │  │  │ MODULE  │  │          │
│  │  └─────────┘  │  │  └─────────┘  │          │
│  │  ┌─────────┐  │  │  ┌─────────┐  │          │
│  │  │ MODULE  │  │  │  │ MODULE  │  │          │
│  │  └─────────┘  │  │  └─────────┘  │          │
│  └───────────────┘  └───────────────┘          │
└─────────────────────────────────────────────────┘
```

### Semantic Evolution Loop

The continuous cycle that enables autonomous, meaningful evolution:

> **Perception → Reasoning → Action → Reflection → Verification → Evolution**

### Core Principles

1. **Context is the Boundary of Intelligence** — Well-defined boundaries enable safe AI reasoning
2. **Knowledge Should Be Local** — All information needed to understand a module is co-located
3. **Meaning Before Mechanics** — Understanding precedes execution
4. **Evolution Through Understanding** — Systems evolve with awareness, not just functionality

---

## 🚀 Getting Started

### For Developers
1. Read the [Vision](docs/vision.md) to understand the philosophy
2. Study the [Semantic Project Model](docs/semantic-project-model.md) to learn the structure
3. Review the [Semantic Collaboration Model](docs/semantic-collaboration-model.md) for workflows
4. Use the [Glossary](docs/glossary.md) as a reference

### For AI Agents
1. Load the [Semantic Collaboration Model](docs/semantic-collaboration-model.md) for protocols
2. Reference the [Semantic Project Model](docs/semantic-project-model.md) for schema specifications
3. Use the [Glossary](docs/glossary.md) for terminology consistency

---

## 🧩 Framework Components

| Component                  | Description                                                   |
| -------------------------- | ------------------------------------------------------------- |
| **Semantic Module**        | Smallest self-contained unit (code + docs + tests)            |
| **Semantic Cluster**       | Domain-level grouping of related modules                      |
| **Semantic Project**       | Complete system or application                                |
| **Semantic Contract**      | Explicit invariants and behavioral guarantees                 |
| **Semantic Stewardship**   | Ownership and accountability for semantic integrity           |
| **Semantic Evolution Loop**| Continuous cycle for meaningful change                        |
| **Semantic Graph**         | Dependency and relationship visualization                     |
| **Semantic Validation**    | Automated consistency checking                                |

---

## 🛠️ Tooling & Integration

The Semantic Architecture supports integration with:

- **CI/CD**: Automated semantic validation and contract checking
- **Version Control**: Semantic commit protocols and change tracking
- **IDEs**: Context-aware navigation and inline contract display
- **AI Systems**: Bounded reasoning contexts for safe agent operation

See [Semantic Project Model: Tooling Integration](docs/semantic-project-model.md#81-semantic-tooling-integration) for details.

### 🌐 MCP Server (NEW)

The **Semantic Architecture MCP Server** transforms this framework into a live semantic context provider:

- **Live Semantic Context**: Real-time access to project structure, validation, and drift detection
- **API Endpoints**: RESTful APIs for semantic graph, validation, glossary, and ADRs
- **AI Integration**: Enables AI agents and tools to query semantic intelligence
- **Cross-Platform**: Supports Linux, macOS, and Windows
- **Deployment Ready**: Supports both local and Docker deployment

**Quick Start:**

**Linux/macOS:**
```bash
# Local deployment
./start-local.sh

# Docker deployment  
./start-docker.sh dev
```

**Windows (PowerShell):**
```powershell
# Local deployment
.\start-local.ps1

# Docker deployment
.\start-docker.ps1 dev
```

**Documentation:**
- [Quick Start Guide](QUICKSTART.md) - Get started in 30 seconds
- [MCP Server README](mcp_server/README.md) - API documentation and usage
- [Deployment Guide](DEPLOYMENT.md) - Complete deployment instructions
- [Testing Guide](tests/README.md) - Comprehensive testing documentation

---

## 📖 Version History

- **2.0** (2025-11-06): Major refinement with unified terminology, cross-references, enhanced examples, visual overviews, and harmonized evolution concepts across all documents
- **1.0**: Initial framework documentation

---

## 🤝 Contributing

When contributing to this framework:

1. Maintain consistency with established terminology (see [Glossary](docs/glossary.md))
2. Ensure cross-references remain valid
3. Follow the semantic commit protocol: `[doc-name] Brief description`
4. Update version numbers and "Last Updated" dates

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Quick Links

- [Vision](docs/vision.md) — Why Semantic Architecture?
- [Project Model](docs/semantic-project-model.md) — What is it made of?
- [Collaboration Model](docs/semantic-collaboration-model.md) — How do we use it?
- [Glossary](docs/glossary.md) — What do these terms mean?
- [MCP Server](mcp_server/README.md) — Live semantic context API
- [Deployment Guide](DEPLOYMENT.md) — Deploy locally or with Docker

---

*This is software designed not just to run, but to be understood.*
