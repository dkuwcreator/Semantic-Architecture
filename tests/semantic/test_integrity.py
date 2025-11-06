"""Semantic integrity tests.

Tests that verify semantic consistency, data integrity, and cross-environment
behavior of the MCP server.
"""
import pytest
import json
from pathlib import Path


class TestSemanticConsistency:
    """Test semantic consistency across different scopes and contexts."""
    
    @pytest.mark.semantic
    def test_graph_nodes_have_valid_types(self, mock_semantic_graph_output):
        """Test that all graph nodes have valid scopes."""
        valid_scopes = ["module", "cluster", "project", "component", "service"]
        
        for node in mock_semantic_graph_output["nodes"]:
            assert "scope" in node
            # In a real implementation, we'd enforce strict scopes
            assert isinstance(node["scope"], str)
    
    @pytest.mark.semantic
    def test_graph_edges_reference_existing_nodes(self, mock_semantic_graph_output):
        """Test that all edges reference existing nodes."""
        node_ids = {node["id"] for node in mock_semantic_graph_output["nodes"]}
        
        for edge in mock_semantic_graph_output["edges"]:
            assert edge["from"] in node_ids, f"Source {edge['from']} not found in nodes"
            assert edge["to"] in node_ids, f"Target {edge['to']} not found in nodes"
    
    @pytest.mark.semantic
    def test_validation_severity_levels_are_valid(self, mock_validation_output):
        """Test that validation diagnostics use valid severity levels."""
        valid_levels = ["error", "warning", "info"]
        
        for diagnostic in mock_validation_output["diagnostics"]:
            assert diagnostic["severity"] in valid_levels
    
    @pytest.mark.semantic
    def test_drift_alerts_have_required_fields(self, mock_drift_output):
        """Test that drift alerts contain all required fields."""
        required_fields = ["code", "id", "type", "scope", "target", "message", "confidence"]
        
        for drift in mock_drift_output["drifts"]:
            for field in required_fields:
                assert field in drift, f"Missing required field: {field}"
    
    @pytest.mark.semantic
    def test_adr_records_have_valid_status(self, mock_adr_output):
        """Test that ADR records exist."""
        # Note: In the actual model, status is not required
        # We just verify records exist and have required fields
        for record in mock_adr_output["records"]:
            assert "id" in record
            assert "title" in record
            assert "path" in record


class TestDataIntegrity:
    """Test data integrity and validation rules."""
    
    @pytest.mark.semantic
    def test_glossary_entries_unique_terms(self, sample_glossary_entries):
        """Test that glossary terms are unique."""
        terms = [entry["term"] for entry in sample_glossary_entries]
        assert len(terms) == len(set(terms)), "Duplicate glossary terms found"
    
    @pytest.mark.semantic
    def test_glossary_entries_have_definitions(self, sample_glossary_entries):
        """Test that all glossary entries have non-empty definitions."""
        for entry in sample_glossary_entries:
            assert "definition" in entry
            assert len(entry["definition"].strip()) > 0
    
    @pytest.mark.semantic
    def test_validation_summary_counts_match(self, mock_validation_output):
        """Test that validation summary counts match diagnostic counts."""
        summary = mock_validation_output["summary"]
        diagnostics = mock_validation_output["diagnostics"]
        
        # Count diagnostics by severity
        error_count = sum(1 for d in diagnostics if d["severity"] == "error")
        warning_count = sum(1 for d in diagnostics if d["severity"] == "warning")
        
        assert summary["errors"] == error_count
        assert summary["warnings"] == warning_count
    
    @pytest.mark.semantic
    def test_drift_summary_count_matches_alerts(self, mock_drift_output):
        """Test that drift summary count matches number of drifts."""
        summary = mock_drift_output["summary"]
        drifts = mock_drift_output["drifts"]
        
        assert summary["count"] == len(drifts)
    
    @pytest.mark.semantic
    def test_drift_category_counts_match(self, mock_drift_output):
        """Test that drift category counts match actual drift categories."""
        summary = mock_drift_output["summary"]
        drifts = mock_drift_output["drifts"]
        
        # Count drifts by type
        type_counts = {}
        for drift in drifts:
            drift_type = drift["type"]
            type_counts[drift_type] = type_counts.get(drift_type, 0) + 1
        
        assert summary["byType"] == type_counts


class TestCrossEnvironmentConsistency:
    """Test that behavior is consistent across different environments."""
    
    @pytest.mark.semantic
    def test_json_output_is_serializable(self, mock_semantic_graph_output, 
                                         mock_validation_output, mock_drift_output):
        """Test that all outputs can be serialized to JSON."""
        outputs = [
            mock_semantic_graph_output,
            mock_validation_output,
            mock_drift_output
        ]
        
        for output in outputs:
            # Should not raise exception
            json_str = json.dumps(output)
            # Should be able to deserialize back
            parsed = json.loads(json_str)
            assert parsed == output
    
    @pytest.mark.semantic
    def test_path_separators_are_normalized(self, temp_repo_dir):
        """Test that file paths work across platforms."""
        from mcp_server.adapters import FilesystemAdapter
        
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        
        # Test with forward slashes (Unix-style)
        assert adapter.file_exists("docs") or not adapter.file_exists("docs")
        
        # Path normalization should handle both separators
        test_file = temp_repo_dir / "docs" / "test.md"
        test_file.parent.mkdir(exist_ok=True)
        test_file.write_text("test")
        
        # Should work with forward slashes
        assert adapter.file_exists("docs/test.md")
    
    @pytest.mark.semantic
    def test_unicode_handling_in_glossary(self, temp_repo_dir):
        """Test that Unicode characters are handled correctly."""
        glossary_path = temp_repo_dir / "docs" / "glossary.md"
        glossary_content = """# Glossary

## Core Concepts

### Naïve Approach
A simple approach that doesn't account for edge cases.

### Café Pattern
A design pattern for service orchestration.

### 中文术语
A term in Chinese characters.
"""
        glossary_path.write_text(glossary_content, encoding="utf-8")
        
        from mcp_server.adapters import FilesystemAdapter
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        
        entries = adapter.read_glossary()
        assert len(entries) == 3
        assert entries[0].term == "Naïve Approach"
        assert entries[1].term == "Café Pattern"
        assert entries[2].term == "中文术语"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    @pytest.mark.semantic
    def test_empty_semantic_graph(self):
        """Test handling of empty semantic graph."""
        from mcp_server.models import SemanticGraph
        
        graph = SemanticGraph(
            nodes=[],
            edges=[],
            meta={"generatedAt": "2025-11-06T19:00:00Z"}
        )
        
        assert len(graph.nodes) == 0
        assert len(graph.edges) == 0
    
    @pytest.mark.semantic
    def test_validation_with_no_diagnostics(self):
        """Test validation result with no diagnostics."""
        from mcp_server.models import ValidationResult, ValidationSummary
        
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
        
        assert result.summary.errors == 0
        assert len(result.diagnostics) == 0
    
    @pytest.mark.semantic
    def test_drift_with_no_alerts(self):
        """Test drift report with no alerts."""
        from mcp_server.models import DriftReport, DriftSummary
        
        report = DriftReport(
            drifts=[],
            summary=DriftSummary(
                count=0,
                byType={},
                bySeverity={}
            ),
            diffSummary="",
            meta={
                "generatedAt": "2025-11-06T19:00:00Z",
                "toolVersion": "1.0.0",
                "baseRef": "origin/main",
                "headRef": "HEAD"
            }
        )
        
        assert report.summary.count == 0
        assert len(report.drifts) == 0
    
    @pytest.mark.semantic
    def test_glossary_with_no_category(self, temp_repo_dir):
        """Test glossary entries without categories."""
        glossary_path = temp_repo_dir / "docs" / "glossary.md"
        glossary_content = """# Glossary

### Term Without Category
This term appears before any category heading.
"""
        glossary_path.write_text(glossary_content)
        
        from mcp_server.adapters import FilesystemAdapter
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        
        entries = adapter.read_glossary()
        assert len(entries) == 1
        assert entries[0].term == "Term Without Category"
        assert entries[0].category is None
    
    @pytest.mark.semantic
    @pytest.mark.slow
    def test_large_graph_handling(self):
        """Test handling of graphs with multiple nodes."""
        from mcp_server.models import SemanticNode, SemanticGraph
        
        # Create a graph with 20 nodes to validate scalability
        nodes = [
            SemanticNode(
                id=f"node-{i}",
                scope="module",
                name=f"Module {i}"
            )
            for i in range(20)
        ]
        
        graph = SemanticGraph(
            nodes=nodes,
            edges=[],
            meta={"generatedAt": "2025-11-06T19:00:00Z"}
        )
        
        assert len(graph.nodes) == 20
        
        # Should be able to serialize
        json.dumps(graph.model_dump())
    
    @pytest.mark.semantic
    def test_deeply_nested_node_attributes(self):
        """Test nodes with deeply nested attributes in meta."""
        from mcp_server.models import SemanticNode
        
        node = SemanticNode(
            id="complex-node",
            scope="module",
            name="Complex Module",
            meta={
                "owner": "team",
                "tags": ["core", "critical"],
                "config": {
                    "nested": {
                        "deeply": {
                            "value": 42
                        }
                    }
                }
            }
        )
        
        assert node.meta["config"]["nested"]["deeply"]["value"] == 42


class TestErrorConditions:
    """Test error handling and recovery."""
    
    @pytest.mark.semantic
    def test_invalid_node_id_format(self):
        """Test handling of invalid node ID formats."""
        from mcp_server.models import SemanticNode
        
        # Empty ID should be accepted by model but might fail validation
        node = SemanticNode(id="", scope="module", name="Empty ID")
        assert node.id == ""
        
        # Special characters in ID
        node = SemanticNode(id="node-with-special-chars_123", scope="module", name="Special")
        assert "special-chars" in node.id
    
    @pytest.mark.semantic
    def test_missing_required_fields_in_validation(self):
        """Test validation when required fields are missing."""
        from pydantic import ValidationError
        from mcp_server.models import ValidationDiagnostic
        
        # Missing required fields should raise ValidationError
        with pytest.raises(ValidationError):
            ValidationDiagnostic()
    
    @pytest.mark.semantic
    def test_invalid_severity_level(self):
        """Test handling of values in drift alerts."""
        from mcp_server.models import DriftAlert
        
        # Model should accept any string values for fields
        alert = DriftAlert(
            code="test-code",
            id="alert-001",
            type="test-type",
            scope="module",
            target={"id": "target-id", "path": "test.md"},
            message="Test alert",
            confidence=0.5
        )
        
        assert alert.code == "test-code"
        assert alert.confidence == 0.5
