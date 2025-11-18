# Semantic Architecture MCP Server

A **Model Context Protocol (MCP)** server that exposes semantic context, validation, drift detection, and architectural intelligence as HTTP endpoints.

## Overview

This MCP server transforms the Semantic Architecture from a static documentation/validation toolkit into a **live semantic context provider**, serving project metadata, architectural decisions, and glossary definitions in real-time.

## Features

- **Semantic Graph API** - Query and visualize the project's semantic structure
- **Validation API** - Validate semantic files and contracts
- **Drift Detection API** - Monitor semantic drift across git references
- **Glossary API** - Access and search glossary terms
- **ADR API** - Index and retrieve Architecture Decision Records

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Verify Python scripts are executable:
```bash
python3 scripts/semantic_graph.py --help
```

## Running the Server

### Development Mode

```bash
python3 -m mcp_server.main
```

Or with uvicorn directly:

```bash
uvicorn mcp_server.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn mcp_server.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Root & Health

- `GET /` - Server information and endpoint listing
- `GET /health` - Health check endpoint

### Semantic Graph

- `GET /semantic/graph` - Get the semantic graph
  - Query params: `scope`, `ids`, `include`, `edgeTypes`, `outputFormat`
- `POST /semantic/graph` - Query with request body

**Example:**
```bash
curl http://localhost:8000/semantic/graph?scope=project
```

### Semantic Validation

- `GET /semantic/validate` - Validate semantic files
  - Query params: `targets`, `scope`, `ruleset`, `fixMode`
- `POST /semantic/validate` - Validate with request body

**Example:**
```bash
curl http://localhost:8000/semantic/validate?ruleset=strict
```

### Drift Detection

- `GET /semantic/drift` - Detect semantic drift
  - Query params: `baseRef`, `headRef`, `scopes`, `includeDiffSummary`, `threshold`
- `POST /semantic/drift` - Detect with request body

**Example:**
```bash
curl "http://localhost:8000/semantic/drift?baseRef=origin/main&headRef=HEAD"
```

### Glossary

- `GET /semantic/glossary` - Get all glossary entries
  - Query params: `category`, `search`
- `GET /semantic/glossary/{term}` - Get specific term

**Example:**
```bash
curl http://localhost:8000/semantic/glossary?category=Core%20Concepts
curl http://localhost:8000/semantic/glossary/Semantic%20Module
```

### ADR Index

- `GET /semantic/adr` - Get ADR index
  - Query params: `root`, `patterns`
- `POST /semantic/adr` - Query with request body

**Example:**
```bash
curl http://localhost:8000/semantic/adr?root=docs
```

## Interactive Documentation

Once the server is running, access interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Architecture

```
mcp_server/
├── main.py                  # FastAPI application entry point
├── config.yaml              # Server configuration
├── routes/                  # API route handlers
│   ├── semantic_graph.py    # Semantic graph endpoints
│   ├── validator.py         # Validation endpoints
│   ├── drift.py             # Drift detection endpoints
│   ├── glossary.py          # Glossary endpoints
│   └── adr.py               # ADR endpoints
├── adapters/                # Data source adapters
│   └── filesystem_adapter.py # Filesystem/script adapter
└── models/                  # Pydantic data models
    ├── semantic_node.py     # Graph models
    ├── validation_result.py # Validation models
    ├── drift_report.py      # Drift models
    ├── adr.py               # ADR models
    └── glossary.py          # Glossary models
```

## Integration with AI Agents

The MCP server enables AI agents and editors (VS Code, Copilot, ChatGPT plugins, etc.) to:

1. Query live semantic context
2. Validate changes against semantic contracts
3. Detect and monitor semantic drift
4. Access glossary definitions for consistent terminology
5. Retrieve architectural decisions

### Example Agent Integration

```python
import requests

# Query semantic graph
response = requests.get("http://localhost:8000/semantic/graph?scope=module")
graph = response.json()

# Validate a module
response = requests.post("http://localhost:8000/semantic/validate", json={
    "targets": ["my-module"],
    "scope": "module",
    "ruleset": "strict"
})
validation = response.json()
```

## Configuration

Edit `mcp_server/config.yaml` to customize:

- Server host and port
- Repository paths
- Logging settings
- CORS policies
- Script execution timeouts

## Security Considerations

**Important**: This is a Phase 1 implementation focused on local development:

- No authentication/authorization implemented yet
- CORS is set to allow all origins (configure for production)
- Intended for local or trusted network use
- Script execution has timeout protection
- Read-only operations (no write endpoints)

For production deployment, implement:
- Authentication (API keys, OAuth, etc.)
- Rate limiting
- Input sanitization
- Restricted CORS origins
- Network isolation

## Development

### Running Tests

```bash
# TODO: Add test suite
pytest tests/
```

### Adding New Endpoints

1. Create a new route file in `mcp_server/routes/`
2. Define Pydantic models in `mcp_server/models/`
3. Register the router in `mcp_server/main.py`

## Future Enhancements

See the issue for the full roadmap. Planned enhancements include:

- **Phase 2**: WebSocket support for real-time drift alerts
- **Phase 3**: Client SDKs and IDE plugins
- **Phase 4**: Governance integration with GitHub Actions
- Caching layer for improved performance
- Authentication and authorization
- Event streaming for semantic updates

## Contributing

When contributing to the MCP server:

1. Follow the Semantic Architecture principles
2. Update this README for new endpoints
3. Add appropriate Pydantic models for type safety
4. Include examples in API documentation
5. Test endpoints with sample data

## License

This MCP server is part of the Semantic Architecture project and is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## References

- [Issue: Turning Semantic Architecture into an MCP Server](../../../issues)
- [Semantic Architecture Documentation](../docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
