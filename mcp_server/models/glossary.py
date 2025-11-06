"""Glossary data models."""
from typing import Optional, List
from pydantic import BaseModel


class GlossaryEntry(BaseModel):
    """A single glossary entry."""
    term: str
    definition: str
    category: Optional[str] = None
    related: List[str] = []
