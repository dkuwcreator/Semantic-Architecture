"""Validation result data models."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DiagnosticLocation(BaseModel):
    """Location of a diagnostic."""
    file: str
    startLine: Optional[int] = Field(default=None, ge=0)
    endLine: Optional[int] = Field(default=None, ge=0)


class RelatedInfo(BaseModel):
    """Related information for a diagnostic."""
    file: str
    message: str


class SuggestedFix(BaseModel):
    """Suggested fix for a diagnostic."""
    patchFormat: str
    patch: str


class ValidationDiagnostic(BaseModel):
    """A single validation diagnostic."""
    severity: str
    code: str
    message: str
    location: DiagnosticLocation
    related: List[RelatedInfo] = Field(default_factory=list)
    suggestedFix: Optional[SuggestedFix] = None


class ValidationSummary(BaseModel):
    """Summary of validation results."""
    errors: int = 0
    warnings: int = 0
    infos: int = 0
    ruleset: str
    scope: Optional[str] = None


class ValidationMeta(BaseModel):
    """Metadata for validation results."""
    generatedAt: str
    toolVersion: str
    schemaVersion: str = "1"


class ValidationResult(BaseModel):
    """Complete validation result."""
    diagnostics: List[ValidationDiagnostic]
    summary: ValidationSummary
    meta: ValidationMeta
