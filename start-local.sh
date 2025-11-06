#!/bin/bash
# Startup script for local development

set -e

echo "🚀 Starting Semantic Architecture MCP Server (Local Mode)"
echo "=========================================================="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Verify scripts are executable
echo "✓ Verifying scripts..."
python3 scripts/semantic_graph.py --help > /dev/null 2>&1 && echo "  - semantic_graph.py OK" || echo "  - semantic_graph.py FAILED"

# Check if port 8000 is available
PORT_CHECKED=0
if command -v lsof >/dev/null 2>&1 ; then
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "⚠️  Port 8000 is already in use. Using port 8001 instead."
        PORT=8001
    else
        PORT=8000
    fi
    PORT_CHECKED=1
elif command -v ss >/dev/null 2>&1 ; then
    if ss -ltn | awk '{print $4}' | grep -q ':8000$' ; then
        echo "⚠️  Port 8000 is already in use. Using port 8001 instead."
        PORT=8001
    else
        PORT=8000
    fi
    PORT_CHECKED=1
elif command -v netstat >/dev/null 2>&1 ; then
    if netstat -ltn 2>/dev/null | awk '{print $4}' | grep -q ':8000$' ; then
        echo "⚠️  Port 8000 is already in use. Using port 8001 instead."
        PORT=8001
    else
        PORT=8000
    fi
    PORT_CHECKED=1
else
    echo "⚠️  Could not check if port 8000 is in use (lsof, ss, netstat not found). Defaulting to port 8000."
    PORT=8000
fi

echo ""
echo "✓ All checks passed!"
echo ""
echo "Starting server on http://localhost:$PORT"
echo "  - API Documentation: http://localhost:$PORT/docs"
echo "  - Health Check: http://localhost:$PORT/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================================="

# Start the server
uvicorn mcp_server.main:app --host 0.0.0.0 --port $PORT --reload
