"""Semantic drift detection API routes."""
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..models import DriftReport
from ..adapters import FilesystemAdapter


router = APIRouter(prefix="/semantic/drift", tags=["semantic"])


class DriftRequest(BaseModel):
    """Request body for drift detection."""
    baseRef: str = "origin/main"
    headRef: str = "HEAD"
    scopes: Optional[List[str]] = None
    includeDiffSummary: bool = True
    threshold: str = "all"


def get_adapter():
    """Dependency to get filesystem adapter."""
    return FilesystemAdapter()


@router.get("", response_model=DriftReport)
async def detect_drift(
    baseRef: str = "origin/main",
    headRef: str = "HEAD",
    scopes: Optional[str] = None,
    includeDiffSummary: bool = True,
    threshold: str = "all",
    adapter: FilesystemAdapter = Depends(get_adapter)
):
    """Detect semantic drift across git refs.
    
    Args:
        baseRef: Base git reference for comparison
        headRef: Head git reference for comparison
        scopes: Comma-separated list of scopes to check
        includeDiffSummary: Include diff summary in response
        threshold: Threshold level (all, error, warning)
        adapter: Filesystem adapter dependency
        
    Returns:
        DriftReport response
    """
    try:
        args = [
            "--baseRef", baseRef,
            "--headRef", headRef,
            "--threshold", threshold
        ]
        
        if scopes:
            args.extend(["--scopes"] + scopes.split(","))
        if includeDiffSummary:
            args.append("--includeDiffSummary")
        
        result = adapter.run_script("semantic_drift_scanner.py", args)
        return DriftReport(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=DriftReport)
async def detect_drift_post(
    request: DriftRequest,
    adapter: FilesystemAdapter = Depends(get_adapter)
):
    """Detect semantic drift with POST request.
    
    Args:
        request: Drift detection request parameters
        adapter: Filesystem adapter dependency
        
    Returns:
        DriftReport response
    """
    try:
        args = [
            "--baseRef", request.baseRef,
            "--headRef", request.headRef,
            "--threshold", request.threshold
        ]
        
        if request.scopes:
            args.extend(["--scopes"] + request.scopes)
        if request.includeDiffSummary:
            args.append("--includeDiffSummary")
        
        result = adapter.run_script("semantic_drift_scanner.py", args)
        return DriftReport(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
