"""Main FastAPI application for the Semantic Architecture MCP Server.

This server exposes semantic context, validation, drift detection, and other
semantic intelligence as HTTP endpoints following the MCP (Model Context Protocol) patterns.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from .routes import (
    semantic_graph_router,
    validator_router,
    glossary_router,
    adr_router,
    drift_router,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Semantic Architecture MCP Server",
    description=(
        "A Model Context Protocol (MCP) server that exposes semantic context, "
        "validation, drift detection, and architectural intelligence for the "
        "Semantic Architecture framework."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with server information."""
    return {
        "name": "Semantic Architecture MCP Server",
        "version": "0.1.0",
        "description": "Semantic context provider for AI collaboration",
        "endpoints": {
            "graph": "/semantic/graph",
            "validate": "/semantic/validate",
            "drift": "/semantic/drift",
            "glossary": "/semantic/glossary",
            "adr": "/semantic/adr",
        },
        "docs": "/docs",
        "status": "operational"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "mcp-server",
        "version": "0.1.0"
    }


# Include routers
app.include_router(semantic_graph_router)
app.include_router(validator_router)
app.include_router(glossary_router)
app.include_router(adr_router)
app.include_router(drift_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
