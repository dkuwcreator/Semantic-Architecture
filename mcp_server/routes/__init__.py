"""Route handlers for the MCP server."""
from .semantic_graph import router as semantic_graph_router
from .validator import router as validator_router
from .glossary import router as glossary_router
from .adr import router as adr_router
from .drift import router as drift_router

__all__ = [
    "semantic_graph_router",
    "validator_router",
    "glossary_router",
    "adr_router",
    "drift_router",
]
