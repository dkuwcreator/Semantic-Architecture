"""Semantic graph API routes."""
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..models import SemanticGraph
from ..adapters import FilesystemAdapter


router = APIRouter(prefix="/semantic/graph", tags=["semantic"])


class GraphQueryParams(BaseModel):
    """Query parameters for semantic graph."""
    scope: Optional[str] = "project"
    ids: Optional[List[str]] = None
    include: Optional[List[str]] = None
    edgeTypes: Optional[List[str]] = None
    outputFormat: Optional[str] = "json"


def get_adapter():
    """Dependency to get filesystem adapter."""
    return FilesystemAdapter()


@router.get("", response_model=SemanticGraph)
async def get_semantic_graph(
    scope: str = "project",
    ids: Optional[str] = None,
    include: Optional[str] = None,
    edgeTypes: Optional[str] = None,
    outputFormat: str = "json",
    adapter: FilesystemAdapter = Depends(get_adapter)
):
    """Get the semantic graph for the project.
    
    Args:
        scope: Scope of the graph (project, cluster, module)
        ids: Comma-separated list of node IDs to include
        include: Comma-separated list of fields to include
        edgeTypes: Comma-separated list of edge types to include
        outputFormat: Output format (json or dot)
        adapter: Filesystem adapter dependency
        
    Returns:
        SemanticGraph response
    """
    try:
        args = ["--scope", scope, "--outputFormat", outputFormat]
        
        if ids:
            args.extend(["--ids"] + ids.split(","))
        if include:
            args.extend(["--include"] + include.split(","))
        if edgeTypes:
            args.extend(["--edgeTypes"] + edgeTypes.split(","))
        
        result = adapter.run_script("semantic_graph.py", args)
        return SemanticGraph(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=SemanticGraph)
async def query_semantic_graph(
    params: GraphQueryParams,
    adapter: FilesystemAdapter = Depends(get_adapter)
):
    """Query the semantic graph with POST request.
    
    Args:
        params: Query parameters
        adapter: Filesystem adapter dependency
        
    Returns:
        SemanticGraph response
    """
    try:
        args = ["--scope", params.scope, "--outputFormat", params.outputFormat]
        
        if params.ids:
            args.extend(["--ids"] + params.ids)
        if params.include:
            args.extend(["--include"] + params.include)
        if params.edgeTypes:
            args.extend(["--edgeTypes"] + params.edgeTypes)
        
        result = adapter.run_script("semantic_graph.py", args)
        return SemanticGraph(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
