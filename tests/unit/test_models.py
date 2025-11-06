"""Unit tests for data models.

Tests the Pydantic models used in the MCP server to ensure proper validation
and serialization/deserialization.
"""
import pytest
from pydantic import ValidationError

from mcp_server.models import (
    SemanticNode,
    SemanticEdge,
    SemanticGraph,
    ValidationDiagnostic,
    ValidationSummary,
    ValidationResult,
    DriftAlert,
    DriftSummary,
    DriftReport,
    ADRRecord,
    ADRIndex,
    GlossaryEntry,
)


class TestSemanticNode:
    """Test SemanticNode model."""
    
    @pytest.mark.unit
    def test_valid_semantic_node(self):
        """Test creating a valid semantic node."""
        node = SemanticNode(
            id="test-node",
            scope="module",
            name="Test Module",
            path="/modules/test",
            owners=["@team-test"]
        )
        assert node.id == "test-node"
        assert node.scope == "module"
        assert node.name == "Test Module"
    
    @pytest.mark.unit
    def test_semantic_node_minimal(self):
        """Test semantic node with minimal required fields."""
        node = SemanticNode(
            id="minimal",
            scope="module"
        )
        assert node.id == "minimal"
        assert node.scope == "module"


class TestSemanticEdge:
    """Test SemanticEdge model."""
    
    @pytest.mark.unit
    def test_valid_semantic_edge(self):
        """Test creating a valid semantic edge."""
        # Using from_node parameter directly since it's aliased
        edge = SemanticEdge(from_node="node-a", to="node-b", type="depends-on")
        assert edge.from_node == "node-a"
        assert edge.to == "node-b"
        assert edge.type == "depends-on"
    
    @pytest.mark.unit
    def test_semantic_edge_minimal(self):
        """Test semantic edge with minimal required fields."""
        edge = SemanticEdge(from_node="a", to="b", type="link")
        assert edge.from_node == "a"
        assert edge.to == "b"


class TestSemanticGraph:
    """Test SemanticGraph model."""
    
    @pytest.mark.unit
    def test_valid_semantic_graph(self, mock_semantic_graph_output):
        """Test creating a valid semantic graph."""
        graph = SemanticGraph(**mock_semantic_graph_output)
        assert len(graph.nodes) == 2
        assert len(graph.edges) == 1
    
    @pytest.mark.unit
    def test_empty_semantic_graph(self):
        """Test creating an empty semantic graph."""
        graph = SemanticGraph(
            nodes=[],
            edges=[],
            meta={"generatedAt": "2025-11-06T19:00:00Z"}
        )
        assert len(graph.nodes) == 0
        assert len(graph.edges) == 0


class TestValidationDiagnostic:
    """Test ValidationDiagnostic model."""
    
    @pytest.mark.unit
    def test_valid_diagnostic(self):
        """Test creating a valid diagnostic."""
        diag = ValidationDiagnostic(
            severity="error",
            code="missing-field",
            message="Missing required field",
            location={
                "file": "test.md",
                "startLine": 10,
                "endLine": 10
            }
        )
        assert diag.severity == "error"
        assert diag.message == "Missing required field"
        assert diag.code == "missing-field"
    
    @pytest.mark.unit
    def test_diagnostic_with_fix(self):
        """Test diagnostic with suggested fix."""
        diag = ValidationDiagnostic(
            severity="warning",
            code="style-issue",
            message="Style issue",
            location={"file": "test.md", "startLine": 5},
            suggestedFix={
                "patchFormat": "unified",
                "patch": "+fixed content"
            }
        )
        assert diag.suggestedFix is not None
        assert diag.suggestedFix.patch == "+fixed content"


class TestValidationSummary:
    """Test ValidationSummary model."""
    
    @pytest.mark.unit
    def test_valid_summary(self):
        """Test creating a valid validation summary."""
        summary = ValidationSummary(
            errors=2,
            warnings=5,
            infos=1,
            ruleset="default"
        )
        assert summary.errors == 2
        assert summary.warnings == 5
        assert summary.ruleset == "default"


class TestValidationResult:
    """Test ValidationResult model."""
    
    @pytest.mark.unit
    def test_valid_result(self, mock_validation_output):
        """Test creating a valid validation result."""
        result = ValidationResult(**mock_validation_output)
        assert result.summary.errors == 0
        assert result.summary.warnings == 1
        assert len(result.diagnostics) == 1
    
    @pytest.mark.unit
    def test_empty_result(self):
        """Test validation result with no diagnostics."""
        result = ValidationResult(
            diagnostics=[],
            summary=ValidationSummary(
                errors=0,
                warnings=0,
                infos=0,
                ruleset="default"
            ),
            meta={
                "generatedAt": "2025-11-06T19:00:00Z",
                "toolVersion": "1.0.0",
                "schemaVersion": "1"
            }
        )
        assert len(result.diagnostics) == 0


class TestDriftAlert:
    """Test DriftAlert model."""
    
    @pytest.mark.unit
    def test_valid_drift_alert(self):
        """Test creating a valid drift alert."""
        alert = DriftAlert(
            code="boundary-change",
            id="alert-001",
            type="structural",
            scope="module",
            target={"id": "module-a", "path": "/modules/a"},
            message="Boundary changed",
            confidence=0.9
        )
        assert alert.code == "boundary-change"
        assert alert.type == "structural"
        assert alert.confidence == 0.9


class TestDriftSummary:
    """Test DriftSummary model."""
    
    @pytest.mark.unit
    def test_valid_drift_summary(self):
        """Test creating a valid drift summary."""
        summary = DriftSummary(
            count=5,
            byType={"structural": 3, "semantic": 2},
            bySeverity={"warning": 4, "info": 1}
        )
        assert summary.count == 5
        assert summary.byType["structural"] == 3


class TestDriftReport:
    """Test DriftReport model."""
    
    @pytest.mark.unit
    def test_valid_drift_report(self, mock_drift_output):
        """Test creating a valid drift report."""
        report = DriftReport(**mock_drift_output)
        assert report.summary.count == 2
        assert len(report.drifts) == 2


class TestADRRecord:
    """Test ADRRecord model."""
    
    @pytest.mark.unit
    def test_valid_adr_record(self):
        """Test creating a valid ADR record."""
        record = ADRRecord(
            id="ADR-001",
            title="Test Decision",
            path="docs/adr-001.md"
        )
        assert record.id == "ADR-001"
        assert record.title == "Test Decision"


class TestADRIndex:
    """Test ADRIndex model."""
    
    @pytest.mark.unit
    def test_valid_adr_index(self, mock_adr_output):
        """Test creating a valid ADR index."""
        index = ADRIndex(**mock_adr_output)
        assert index.meta.count == 2
        assert len(index.records) == 2


class TestGlossaryEntry:
    """Test GlossaryEntry model."""
    
    @pytest.mark.unit
    def test_valid_glossary_entry(self):
        """Test creating a valid glossary entry."""
        entry = GlossaryEntry(
            term="Test Term",
            definition="A test definition",
            category="Testing"
        )
        assert entry.term == "Test Term"
        assert entry.definition == "A test definition"
        assert entry.category == "Testing"
    
    @pytest.mark.unit
    def test_glossary_entry_without_category(self):
        """Test glossary entry without category."""
        entry = GlossaryEntry(
            term="Uncategorized",
            definition="No category specified"
        )
        assert entry.term == "Uncategorized"
        assert entry.category is None or entry.category == ""
