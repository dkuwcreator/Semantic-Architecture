"""Drift report data models."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DriftTarget(BaseModel):
    """Target of a drift alert."""
    id: str
    path: str


class DriftAlert(BaseModel):
    """A single drift alert."""
    code: str
    id: str
    type: str
    scope: str
    target: DriftTarget
    message: str
    confidence: float = Field(ge=0.0, le=1.0)


class DriftSummary(BaseModel):
    """Summary of drift alerts."""
    count: int
    byType: Dict[str, int] = Field(default_factory=dict)
    bySeverity: Dict[str, int] = Field(default_factory=dict)


class DriftMeta(BaseModel):
    """Metadata for drift report."""
    generatedAt: str
    toolVersion: str
    baseRef: str
    headRef: str


class DriftReport(BaseModel):
    """Complete drift report."""
    drifts: List[DriftAlert]
    summary: DriftSummary
    diffSummary: str
    meta: DriftMeta
