# Semantic Architecture MCP Server

This directory contains the Model Context Protocol (MCP) server for the Semantic Architecture project.

## What is this?

This MCP server exposes the Semantic Architecture framework's documentation and tooling to AI assistants like GitHub Copilot through the Model Context Protocol. It provides:

### Resources
- **project-vision**: The VISION.md document
- **collaboration-model**: The Semantic Collaboration Model document
- **project-model**: The Semantic Project Model document

### Tools
- **semantic.map**: Build a hierarchical map of Project → Cluster → Module structure
- **semantic.validate**: Validate that semantic modules contain required documentation
- **semantic.initModule**: Scaffold a new semantic module with proper structure

## Quick Start

### Local Development

```bash
# Install dependencies
npm install

# Build the server
npm run build

# Start the server
npm start
```

The server will run on `http://localhost:3000/mcp`.

### Using with VS Code / GitHub Copilot

Create a `.vscode/mcp.json` file in your workspace:

```json
{
  "servers": {
    "semantic-architecture": {
      "type": "http",
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

### Using with Docker

```bash
# Build the Docker image
docker build -t semantic-architecture-mcp:latest .

# Run the container
docker run --rm -p 3000:3000 semantic-architecture-mcp:latest
```

## Publishing

To publish to GitHub Container Registry:

```bash
# Build and tag
docker build -t ghcr.io/dkuwcreator/semantic-architecture-mcp:0.1.0 .

# Push to registry
docker push ghcr.io/dkuwcreator/semantic-architecture-mcp:0.1.0
```

## Development

```bash
# Watch mode for development
npm run dev
```

## Configuration

The server uses these environment variables:

- `PORT`: HTTP server port (default: 3000)
- `REPO_ROOT`: Path to the repository root (auto-detected in normal use)
