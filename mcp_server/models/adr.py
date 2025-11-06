"""ADR (Architecture Decision Record) data models."""
from typing import List
from pydantic import BaseModel


class ADRRecord(BaseModel):
    """A single ADR record."""
    id: str
    title: str
    path: str


class ADRMeta(BaseModel):
    """Metadata for ADR index."""
    generatedAt: str
    count: int


class ADRIndex(BaseModel):
    """Complete ADR index."""
    records: List[ADRRecord]
    meta: ADRMeta
