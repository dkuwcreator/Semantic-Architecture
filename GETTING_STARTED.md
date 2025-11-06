# Getting Started with the Semantic Architecture MCP Server

This guide will help you set up and use the Model Context Protocol (MCP) server for the Semantic Architecture framework with GitHub Copilot and other MCP-compatible AI assistants.

## What You Get

### Resources
The MCP server exposes three key resources that can be added to AI context:

1. **project-vision** - The VISION.md document explaining the framework
2. **collaboration-model** - The Semantic Collaboration Model
3. **project-model** - The Semantic Project Model

### Tools
Three powerful tools for working with semantic architectures:

1. **semantic-map** - Scans and maps your Project → Cluster → Module hierarchy
2. **semantic-validate** - Validates semantic modules have required documentation
3. **semantic-init-module** - Scaffolds new semantic modules with proper structure

## Quick Start (3 Steps)

### Step 1: Start the MCP Server

**Option A: Using npm (for development)**
```bash
cd mcp-server
npm install
npm run build
npm start
```

**Option B: Using Docker (HTTP mode for testing)**
```bash
docker-compose up -d
```

This starts the server in HTTP mode at `http://localhost:3000/mcp` (useful for testing with curl).

**Option C: Using Docker directly (stdio mode for VS Code)**
```bash
docker build -t semantic-architecture-mcp-server .
# Server uses stdio by default, used by VS Code configuration
```

**Option D: Using Docker directly (HTTP mode)**
```bash
docker build -t semantic-architecture-mcp-server .
docker run -p 3000:3000 semantic-architecture-mcp-server --http
```

For VS Code integration, the stdio mode (used by the `.vscode/mcp.json` configuration) is recommended.

### Step 2: Configure VS Code

The repository includes a pre-configured `.vscode/mcp.json` file that uses Docker with stdio transport:

```json
{
  "servers": {
    "semantic-architecture": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v",
        "${workspaceFolder}:/workspace",
        "-e",
        "REPO_ROOT=/workspace",
        "semantic-architecture-mcp-server"
      ]
    }
  }
}
```

**Alternative: HTTP Transport**

If you prefer HTTP transport (e.g., for remote access), you can:

1. Start the server in HTTP mode:
   ```bash
   docker run -p 3000:3000 semantic-architecture-mcp-server --http
   ```

2. Use this configuration:
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

   Note: HTTP transport may have limitations with VS Code's MCP client. Stdio transport (default) is recommended.

### Step 3: Use with GitHub Copilot

1. **Open VS Code** in any project where you want to use semantic architecture
2. **Open Copilot Chat**
3. **Access MCP Tools**: Click the wrench icon to see available tools
4. **Add MCP Resources**: Use "Add context → MCP Resources" to pull in documentation

## Using the Tools

### Building a Semantic Map

In Copilot Chat, you can ask:
> "Use the semantic-map tool to show me the project structure"

This will scan your repository for clusters and modules.

### Validating Your Structure

> "Use semantic-validate to check if all modules have proper documentation"

This ensures each module has both `about.md` and `semantic-instructions.md`.

### Creating a New Module

> "Use semantic-init-module to create a new module called 'user-auth' in the 'security' cluster"

This scaffolds a properly structured semantic module.

## Working with Chat Modes

The repository includes three AI agent modes:

### Local Agent Mode
For changes within a single module:
```
@workspace /chatmode local-agent
```
- Focused on one module
- Maintains module boundaries
- Preserves contracts and invariants

### Domain Agent Mode
For coordinating across related modules in a cluster:
```
@workspace /chatmode domain-agent
```
- Works across multiple modules
- Maintains consistency
- Manages cluster-level dependencies

### System Architect Mode
For project-wide architectural decisions:
```
@workspace /chatmode system-architect
```
- Maintains overall coherence
- Enforces semantic principles
- Guides architectural evolution

## Using Prompts

The repository includes reusable prompts in `.github/prompts/`:

- **create-module.prompt.md** - Template for creating new modules
- **validate-structure.prompt.md** - Template for validation checks

Use them in Copilot Chat with:
```
@workspace #file:create-module.prompt.md
```

## GitHub Copilot Instructions

The `.github/copilot-instructions.md` file provides project-wide context to Copilot, ensuring it understands:
- The Semantic Architecture principles
- Documentation standards
- Change policies
- Testing procedures

This applies automatically when Copilot works in your repository.

## Publishing to Container Registry

To share the MCP server with your team:

```bash
# Build and tag (build from repo root with -f flag)
docker build -f mcp-server/Dockerfile -t ghcr.io/YOUR_ORG/semantic-architecture-mcp:0.1.0 .

# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Push
docker push ghcr.io/YOUR_ORG/semantic-architecture-mcp:0.1.0
```

Then team members can use in their `.vscode/mcp.json`:
```json
{
  "servers": {
    "semantic-architecture": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v",
        "${workspaceFolder}:/workspace",
        "-e",
        "REPO_ROOT=/workspace",
        "ghcr.io/YOUR_ORG/semantic-architecture-mcp:0.1.0"
      ]
    }
  }
}
```

## Troubleshooting

### Server won't start
```bash
# Check if port 3000 is already in use
lsof -i :3000

# Try a different port
PORT=3001 npm start
```

### MCP tools not showing in VS Code
1. Ensure the server is running: `curl http://localhost:3000/mcp`
2. Restart VS Code
3. Check VS Code's Output panel for MCP logs

### Health Check
```bash
cd mcp-server
npm start &
sleep 2
node test-health.mjs
```

## Next Steps

1. **Read the Documentation**: 
   - [VISION.md](../VISION.md) - The framework vision
   - [Semantic Project Model.md](../Semantic%20Project%20Model.md) - Project structure
   - [Semantic Collaboration Model.md](../Semantic%20Collaboration%20Model.md) - AI collaboration

2. **Try the Tools**: Experiment with semantic.map and semantic.validate in your projects

3. **Create Modules**: Use semantic.initModule to start building semantic architectures

4. **Share with Your Team**: Publish the Docker image and share the configuration

## Support

For issues or questions:
- Open an issue on GitHub
- Check the [MCP SDK documentation](https://github.com/modelcontextprotocol/typescript-sdk)
- Review the [VS Code MCP documentation](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)

## Contributing

We welcome contributions! When contributing:
- Follow the Semantic Architecture principles
- Update documentation alongside code
- Test changes locally before submitting
- See `.github/copilot-instructions.md` for guidelines
