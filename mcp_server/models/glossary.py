"""Glossary data models."""
from typing import Optional
from pydantic import BaseModel


class GlossaryEntry(BaseModel):
    """A single glossary entry."""
    term: str
    definition: str
    category: Optional[str] = None
    related: list[str] = []
