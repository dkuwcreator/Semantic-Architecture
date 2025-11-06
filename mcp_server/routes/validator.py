"""Semantic validator API routes."""
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..models import ValidationResult
from ..adapters import FilesystemAdapter


router = APIRouter(prefix="/semantic/validate", tags=["semantic"])


class ValidateRequest(BaseModel):
    """Request body for validation."""
    targets: Optional[List[str]] = None
    scope: Optional[str] = None
    ruleset: str = "default"
    fixMode: str = "suggest"


def get_adapter():
    """Dependency to get filesystem adapter."""
    return FilesystemAdapter()


@router.get("", response_model=ValidationResult)
async def validate_semantic(
    targets: Optional[str] = None,
    scope: Optional[str] = None,
    ruleset: str = "default",
    fixMode: str = "suggest",
    adapter: FilesystemAdapter = Depends(get_adapter)
):
    """Validate semantic files and contracts.
    
    Args:
        targets: Comma-separated list of targets to validate
        scope: Scope of validation (project, cluster, module)
        ruleset: Validation ruleset (default, strict, ci)
        fixMode: Fix mode (none, suggest)
        adapter: Filesystem adapter dependency
        
    Returns:
        ValidationResult response
    """
    try:
        args = ["--ruleset", ruleset, "--fixMode", fixMode, "--outputFormat", "json"]
        
        if targets:
            args.extend(["--targets"] + targets.split(","))
        if scope:
            args.extend(["--scope", scope])
        
        result = adapter.run_script("semantic_validator.py", args)
        return ValidationResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=ValidationResult)
async def validate_semantic_post(
    request: ValidateRequest,
    adapter: FilesystemAdapter = Depends(get_adapter)
):
    """Validate semantic files with POST request.
    
    Args:
        request: Validation request parameters
        adapter: Filesystem adapter dependency
        
    Returns:
        ValidationResult response
    """
    try:
        args = [
            "--ruleset", request.ruleset,
            "--fixMode", request.fixMode,
            "--outputFormat", "json"
        ]
        
        if request.targets:
            args.extend(["--targets"] + request.targets)
        if request.scope:
            args.extend(["--scope", request.scope])
        
        result = adapter.run_script("semantic_validator.py", args)
        return ValidationResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
