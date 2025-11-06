"""Glossary API routes."""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends

from ..models import GlossaryEntry
from ..adapters import FilesystemAdapter


router = APIRouter(prefix="/semantic/glossary", tags=["semantic"])


def get_adapter():
    """Dependency to get filesystem adapter."""
    return FilesystemAdapter()


@router.get("", response_model=List[GlossaryEntry])
async def get_glossary(
    category: Optional[str] = None,
    search: Optional[str] = None,
    adapter: FilesystemAdapter = Depends(get_adapter)
):
    """Get glossary entries.
    
    Args:
        category: Filter by category
        search: Search term in term or definition
        adapter: Filesystem adapter dependency
        
    Returns:
        List of glossary entries
    """
    try:
        entries = adapter.read_glossary()
        
        # Apply filters
        if category:
            entries = [e for e in entries if e.category and category.lower() in e.category.lower()]
        
        if search:
            search_lower = search.lower()
            entries = [
                e for e in entries
                if search_lower in e.term.lower() or search_lower in e.definition.lower()
            ]
        
        return entries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{term}", response_model=GlossaryEntry)
async def get_glossary_term(
    term: str,
    adapter: FilesystemAdapter = Depends(get_adapter)
):
    """Get a specific glossary term.
    
    Args:
        term: The term to look up
        adapter: Filesystem adapter dependency
        
    Returns:
        Glossary entry
    """
    try:
        entries = adapter.read_glossary()
        
        # Find exact or case-insensitive match
        for entry in entries:
            if entry.term.lower() == term.lower():
                return entry
        
        raise HTTPException(status_code=404, detail=f"Term '{term}' not found in glossary")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
