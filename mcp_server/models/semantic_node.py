"""Semantic graph data models."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class SemanticContract(BaseModel):
    """Semantic contract for a node."""
    invariants: List[str] = Field(default_factory=list)
    validation: Dict[str, Any] = Field(default_factory=dict)


class SemanticNode(BaseModel):
    """A node in the semantic graph."""
    id: str
    scope: str
    name: Optional[str] = None
    path: Optional[str] = None
    owners: List[str] = Field(default_factory=list)
    contract: SemanticContract = Field(default_factory=SemanticContract)
    meta: Optional[Dict[str, Any]] = None


class SemanticEdge(BaseModel):
    """An edge in the semantic graph."""
    model_config = ConfigDict(populate_by_name=True)
    
    from_node: str = Field(alias="from")
    to: str
    type: str
    label: Optional[str] = None
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class GraphMeta(BaseModel):
    """Metadata for the semantic graph."""
    generatedAt: Optional[str] = None
    toolVersion: Optional[str] = None
    projectVersion: Optional[str] = None
    filtersApplied: Optional[Dict[str, Any]] = None


class SemanticGraph(BaseModel):
    """Complete semantic graph response."""
    nodes: List[SemanticNode]
    edges: List[SemanticEdge]
    meta: GraphMeta
