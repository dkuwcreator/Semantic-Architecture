# Quick Start: MCP Server

## 🚀 Get Started in 30 Seconds

### Local Development

**Linux/macOS:**
```bash
./start-local.sh
```

**Windows (PowerShell):**
```powershell
.\start-local.ps1
```

Access at: http://localhost:8000

### Docker Development

**Linux/macOS:**
```bash
./start-docker.sh dev
```

**Windows (PowerShell):**
```powershell
.\start-docker.ps1 dev
```

### Docker Production

**Linux/macOS:**
```bash
./start-docker.sh prod
```

**Windows (PowerShell):**
```powershell
.\start-docker.ps1 prod
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

### Port already in use

**Linux/macOS:**
```bash
# Kill existing server
pkill -f uvicorn

# Or use different port
uvicorn mcp_server.main:app --port 8001
```

**Windows (PowerShell):**
```powershell
# Find and kill process using port 8000
Get-Process -Name python | Where-Object {$_.Path -like "*uvicorn*"} | Stop-Process

# Or use different port
.\start-local.ps1 -Port 8001
```

### Dependencies issue

**Linux/macOS:**
```bash
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
pip install -r requirements.txt
```

### Docker issue

**Linux/macOS:**
```bash
docker-compose down
docker-compose up --build
```

**Windows (PowerShell):**
```powershell
docker-compose down
docker-compose up --build
# or
docker compose down
docker compose up --build
```

## 🔒 Security Notes

- Phase 1 is for development/trusted networks
- Implement authentication before production
- Restrict CORS origins in production
- See [DEPLOYMENT.md](DEPLOYMENT.md#security-considerations)
