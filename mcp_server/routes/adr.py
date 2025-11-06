"""ADR (Architecture Decision Records) API routes."""
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..models import ADRIndex
from ..adapters import FilesystemAdapter


router = APIRouter(prefix="/semantic/adr", tags=["semantic"])


class ADRQueryParams(BaseModel):
    """Query parameters for ADR index."""
    root: str = "docs"
    patterns: Optional[List[str]] = None


def get_adapter():
    """Dependency to get filesystem adapter."""
    return FilesystemAdapter()


@router.get("", response_model=ADRIndex)
async def get_adr_index(
    root: str = "docs",
    patterns: Optional[str] = None,
    adapter: FilesystemAdapter = Depends(get_adapter)
):
    """Get the ADR index for the project.
    
    Args:
        root: Root directory to search for ADRs
        patterns: Comma-separated list of glob patterns
        adapter: Filesystem adapter dependency
        
    Returns:
        ADRIndex response
    """
    try:
        args = ["--root", root]
        
        if patterns:
            args.extend(["--patterns"] + patterns.split(","))
        
        result = adapter.run_script("adr_index.py", args)
        return ADRIndex(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=ADRIndex)
async def query_adr_index(
    params: ADRQueryParams,
    adapter: FilesystemAdapter = Depends(get_adapter)
):
    """Query the ADR index with POST request.
    
    Args:
        params: Query parameters
        adapter: Filesystem adapter dependency
        
    Returns:
        ADRIndex response
    """
    try:
        args = ["--root", params.root]
        
        if params.patterns:
            args.extend(["--patterns"] + params.patterns)
        
        result = adapter.run_script("adr_index.py", args)
        return ADRIndex(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
