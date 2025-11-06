# Deployment Guide: Semantic Architecture MCP Server

Complete guide for deploying the Semantic Architecture MCP Server in both local and containerized environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [Configuration](#configuration)
- [Production Deployment](#production-deployment)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### For Local Deployment

- **Python 3.12+** (Python 3.10+ should work but 3.12 is recommended)
- **pip** (Python package manager)
- **git** (for drift detection features)
- **Virtual environment** (recommended)

### For Docker Deployment

- **Docker 20.10+**
- **Docker Compose 2.0+**
- **4GB+ RAM** (recommended for production)
- **2+ CPU cores** (recommended for production)

### System Requirements

- **Operating System**: Linux, macOS, or Windows (WSL2 for Windows)
- **Disk Space**: 500MB minimum (for dependencies and container images)
- **Network**: Internet connection for initial setup (to pull dependencies)

---

## Local Deployment

### Quick Start (Automated)

Use the provided startup script for the easiest setup:

```bash
./start-local.sh
```

This script will:
1. Check Python version
2. Create and activate a virtual environment
3. Install all dependencies
4. Verify scripts are working
5. Start the server with hot-reload

The server will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Manual Setup

If you prefer manual setup or need more control:

#### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Verify Installation

```bash
# Test Python scripts
python3 scripts/semantic_graph.py --help
python3 scripts/semantic_validator.py --help

# Test MCP server imports
python3 -c "from mcp_server.main import app; print('✓ MCP server ready')"
```

#### 4. Start the Server

**Development mode** (with hot-reload):
```bash
uvicorn mcp_server.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode** (multiple workers):
```bash
uvicorn mcp_server.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 5. Verify Server is Running

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "mcp-server",
  "version": "0.1.0"
}
```

---

## Docker Deployment

### Quick Start (Automated)

Use the provided Docker startup script:

**Development mode** (with hot-reload and volume mounting):
```bash
./start-docker.sh dev
```

**Production mode** (optimized, background):
```bash
./start-docker.sh prod
```

**Stop containers**:
```bash
./start-docker.sh stop
```

### Manual Docker Commands

#### Development Build & Run

```bash
# Build the development image
docker build --target development -t semantic-mcp:dev .

# Run the development container
docker run -d \
  --name semantic-mcp-dev \
  -p 8000:8000 \
  -v $(pwd)/mcp_server:/app/mcp_server \
  -v $(pwd)/scripts:/app/scripts \
  -v $(pwd)/docs:/app/docs \
  -v $(pwd)/data:/app/data \
  -e PYTHONUNBUFFERED=1 \
  semantic-mcp:dev
```

#### Production Build & Run

```bash
# Build the production image
docker build --target production -t semantic-mcp:prod .

# Run the production container
docker run -d \
  --name semantic-mcp-prod \
  -p 8000:8000 \
  -e PYTHONUNBUFFERED=1 \
  --restart unless-stopped \
  semantic-mcp:prod
```

#### Using Docker Compose

The repository includes a `docker-compose.yml` with pre-configured services:

```bash
# Development mode
docker-compose up mcp-server-dev

# Production mode (background)
docker-compose up -d mcp-server-prod

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### Container Management

**View running containers**:
```bash
docker ps
```

**View logs**:
```bash
# Follow logs
docker logs -f semantic-mcp-prod

# Last 100 lines
docker logs --tail 100 semantic-mcp-prod
```

**Execute commands in container**:
```bash
docker exec -it semantic-mcp-prod bash
```

**Restart container**:
```bash
docker restart semantic-mcp-prod
```

**Health check status**:
```bash
docker inspect --format='{{.State.Health.Status}}' semantic-mcp-prod
```

---

## Configuration

### Environment Variables

Configure the server using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `PORT` | Server port | `8000` |
| `HOST` | Server host | `0.0.0.0` |
| `WORKERS` | Number of worker processes (production) | `4` |
| `PYTHONUNBUFFERED` | Enable unbuffered Python output | `1` |

**Example with environment variables**:

```bash
# Local
export LOG_LEVEL=DEBUG
uvicorn mcp_server.main:app --reload

# Docker
docker run -e LOG_LEVEL=DEBUG -e WORKERS=2 semantic-mcp:prod
```

### Server Configuration

Edit `mcp_server/config.yaml` to customize:

```yaml
server:
  host: "0.0.0.0"
  port: 8000
  workers: 4

repository:
  root: "."
  scripts: "scripts"
  docs: "docs"

logging:
  level: "INFO"

cors:
  allow_origins: ["*"]  # Restrict in production!
```

### CORS Configuration

**⚠️ Security Warning**: The default CORS configuration allows all origins. For production, restrict to your specific domains:

```python
# In mcp_server/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://api.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## Production Deployment

### Best Practices

1. **Use Docker** for consistent deployment across environments
2. **Enable authentication** (see Security section below)
3. **Configure CORS** properly for your domain
4. **Use a reverse proxy** (nginx, Traefik) for SSL/TLS
5. **Set up monitoring** and alerting
6. **Configure resource limits** (CPU, memory)
7. **Enable health checks** for automatic restarts

### Deployment with Reverse Proxy (nginx)

**nginx configuration example**:

```nginx
upstream mcp_backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/ssl/certs/yourdomain.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.key;

    location / {
        proxy_pass http://mcp_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://mcp_backend/health;
        access_log off;
    }
}
```

### Security Considerations

**⚠️ Important**: Phase 1 implementation has minimal security features.

**For production, implement**:

1. **Authentication/Authorization**
   - API keys
   - OAuth 2.0
   - JWT tokens

2. **Rate Limiting**
   ```python
   from slowapi import Limiter
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   ```

3. **Input Validation**
   - All inputs are validated via Pydantic models
   - Additional sanitization for git refs

4. **Network Security**
   - Use HTTPS/TLS in production
   - Restrict CORS origins
   - Firewall rules for port 8000

5. **Container Security**
   - Run as non-root user (already configured)
   - Use minimal base images
   - Regular security updates

### Scaling

**Horizontal Scaling with Docker Compose**:

```yaml
services:
  mcp-server:
    build:
      context: .
      target: production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 512M
    ports:
      - "8000-8002:8000"
```

**With Load Balancer**:
- Use nginx, HAProxy, or cloud load balancers
- Enable session affinity if needed
- Configure health checks

---

## Monitoring & Maintenance

### Health Checks

**Local health check**:
```bash
curl http://localhost:8000/health
```

**Docker health check** (automatic):
```bash
docker inspect --format='{{.State.Health.Status}}' semantic-mcp-prod
```

### Logging

**View application logs**:

```bash
# Local (stdout)
# Logs appear in terminal

# Docker
docker logs -f semantic-mcp-prod

# Docker Compose
docker-compose logs -f mcp-server-prod
```

**Log levels**:
- `DEBUG`: Detailed information for debugging
- `INFO`: General informational messages (default)
- `WARNING`: Warning messages
- `ERROR`: Error messages

### Performance Monitoring

**Check resource usage**:

```bash
# Docker stats
docker stats semantic-mcp-prod

# Container resource limits
docker inspect semantic-mcp-prod | jq '.[0].HostConfig.Memory'
```

**Endpoint performance**:
- Use the `/docs` endpoint to test response times
- Monitor slow endpoints
- Check script execution times

### Maintenance Tasks

**Update dependencies**:
```bash
pip install -r requirements.txt --upgrade
```

**Rebuild Docker image**:
```bash
docker-compose build --no-cache
docker-compose up -d
```

**Clean up Docker resources**:
```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Full cleanup
docker system prune -a
```

---

## Troubleshooting

### Common Issues

#### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000
# Or
netstat -tulpn | grep 8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn mcp_server.main:app --port 8001
```

#### Import Errors

**Error**: `ModuleNotFoundError: No module named 'mcp_server'`

**Solution**:
```bash
# Ensure you're in the repository root
cd /path/to/Semantic-Architecture

# Reinstall dependencies
pip install -r requirements.txt

# Verify Python path
python3 -c "import sys; print(sys.path)"
```

#### Script Execution Failures

**Error**: `Script execution failed` or `Script not found`

**Solution**:
```bash
# Verify scripts exist
ls -la scripts/

# Test scripts directly
python3 scripts/semantic_graph.py --help

# Check permissions
chmod +x scripts/*.py
```

#### Docker Build Failures

**Error**: Docker build fails

**Solution**:
```bash
# Clean build without cache
docker build --no-cache -t semantic-mcp:prod .

# Check Docker resources
docker system df

# Prune unused resources
docker system prune -a
```

#### Container Health Check Failing

**Error**: Container marked as unhealthy

**Solution**:
```bash
# Check container logs
docker logs semantic-mcp-prod

# Execute health check manually
docker exec semantic-mcp-prod python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Restart container
docker restart semantic-mcp-prod
```

### Debug Mode

**Enable debug logging**:

```bash
# Local
LOG_LEVEL=DEBUG uvicorn mcp_server.main:app --reload

# Docker
docker run -e LOG_LEVEL=DEBUG semantic-mcp:dev
```

**Test individual endpoints**:

```bash
# Test semantic graph
curl -v http://localhost:8000/semantic/graph?scope=project

# Test validation
curl -v http://localhost:8000/semantic/validate?ruleset=strict

# Test glossary
curl -v http://localhost:8000/semantic/glossary
```

### Getting Help

If issues persist:

1. Check the logs for detailed error messages
2. Verify all prerequisites are installed
3. Ensure you're using the correct Python version
4. Review the [MCP Server README](mcp_server/README.md)
5. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Environment details (OS, Python version, Docker version)
   - Relevant logs

---

## Quick Reference

### Local Deployment Commands

```bash
# Automated startup
./start-local.sh

# Manual startup
source venv/bin/activate
uvicorn mcp_server.main:app --reload

# Test endpoint
curl http://localhost:8000/health
```

### Docker Deployment Commands

```bash
# Development mode
./start-docker.sh dev

# Production mode
./start-docker.sh prod

# Stop containers
./start-docker.sh stop

# View logs
docker-compose logs -f

# Rebuild
docker-compose up --build -d
```

### Health & Status

```bash
# Check server health
curl http://localhost:8000/health

# Check Docker container health
docker inspect --format='{{.State.Health.Status}}' semantic-mcp-prod

# View logs
docker logs -f semantic-mcp-prod

# Check resource usage
docker stats semantic-mcp-prod
```

---

## Additional Resources

- [MCP Server README](mcp_server/README.md) - API documentation
- [Semantic Architecture Documentation](docs/) - Framework overview
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Web framework docs
- [Docker Documentation](https://docs.docker.com/) - Container platform docs
- [Uvicorn Documentation](https://www.uvicorn.org/) - ASGI server docs
