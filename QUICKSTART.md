# Quick Start: MCP Server

## 🚀 Get Started in 30 Seconds

### Local Development
```bash
./start-local.sh
```
Access at: http://localhost:8000

### Docker Development
```bash
./start-docker.sh dev
```

### Docker Production
```bash
./start-docker.sh prod
```

## 📡 Key Endpoints

| Endpoint | Purpose | Example |
|----------|---------|---------|
| `GET /health` | Health check | `curl localhost:8000/health` |
| `GET /semantic/graph` | Get semantic structure | `curl localhost:8000/semantic/graph?scope=project` |
| `GET /semantic/validate` | Validate semantic files | `curl localhost:8000/semantic/validate?ruleset=strict` |
| `GET /semantic/glossary` | Access glossary | `curl localhost:8000/semantic/glossary` |
| `GET /semantic/adr` | Get ADR index | `curl localhost:8000/semantic/adr` |

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (interactive)
- **Full Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **MCP Server**: [mcp_server/README.md](mcp_server/README.md)

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Kill existing server
pkill -f uvicorn

# Or use different port
uvicorn mcp_server.main:app --port 8001
```

**Dependencies issue?**
```bash
pip install -r requirements.txt
```

**Docker issue?**
```bash
docker-compose down
docker-compose up --build
```

## 🔒 Security Notes

- Phase 1 is for development/trusted networks
- Implement authentication before production
- Restrict CORS origins in production
- See [DEPLOYMENT.md](DEPLOYMENT.md#security-considerations)
