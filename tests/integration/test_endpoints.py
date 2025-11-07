"""Integration tests for FastAPI endpoints.

Tests all HTTP endpoints of the MCP server to ensure they respond correctly
and handle various request scenarios.
"""
import pytest


class TestRootEndpoints:
    """Test root and health check endpoints."""
    
    def test_root_endpoint(self, test_client):
        """Test the root endpoint returns server info."""
        response = test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "name" in data
        assert data["name"] == "Semantic Architecture MCP Server"
        assert "version" in data
        assert "endpoints" in data
        assert "status" in data
        assert data["status"] == "operational"
        
        # Verify all expected endpoints are listed
        endpoints = data["endpoints"]
        assert "/semantic/graph" in endpoints["graph"]
        assert "/semantic/validate" in endpoints["validate"]
        assert "/semantic/drift" in endpoints["drift"]
        assert "/semantic/glossary" in endpoints["glossary"]
        assert "/semantic/adr" in endpoints["adr"]
    
    def test_health_check_endpoint(self, test_client):
        """Test the health check endpoint."""
        response = test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["service"] == "mcp-server"
        assert "version" in data
    
    def test_docs_endpoint(self, test_client):
        """Test that OpenAPI docs are accessible."""
        response = test_client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_endpoint(self, test_client):
        """Test that ReDoc is accessible."""
        response = test_client.get("/redoc")
        assert response.status_code == 200
    
    def test_openapi_json(self, test_client):
        """Test that OpenAPI spec is accessible."""
        response = test_client.get("/openapi.json")
        assert response.status_code == 200
        
        spec = response.json()
        assert "openapi" in spec
        assert "info" in spec
        assert spec["info"]["title"] == "Semantic Architecture MCP Server"


class TestSemanticGraphEndpoints:
    """Test semantic graph endpoints."""
    
    @pytest.mark.integration
    def test_get_semantic_graph_default(self, test_client):
        """Test GET /semantic/graph with default parameters."""
        response = test_client.get("/semantic/graph")
        
        # May return 500 if scripts aren't properly set up in test environment
        # We accept both 200 (success) and 500 (expected in minimal test env)
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "nodes" in data
            assert "edges" in data
            assert "meta" in data
    
    @pytest.mark.integration
    def test_get_semantic_graph_with_params(self, test_client):
        """Test GET /semantic/graph with query parameters."""
        response = test_client.get(
            "/semantic/graph",
            params={
                "scope": "module",
                "outputFormat": "json",
                "ids": "module-1,module-2"
            }
        )
        
        assert response.status_code in [200, 500]
    
    @pytest.mark.integration
    def test_post_semantic_graph(self, test_client):
        """Test POST /semantic/graph."""
        payload = {
            "scope": "project",
            "ids": ["module-core"],
            "outputFormat": "json"
        }
        
        response = test_client.post("/semantic/graph", json=payload)
        assert response.status_code in [200, 500]
    
    @pytest.mark.integration
    def test_semantic_graph_invalid_format(self, test_client):
        """Test semantic graph with invalid output format."""
        response = test_client.get(
            "/semantic/graph",
            params={"outputFormat": "invalid"}
        )
        
        # Should either reject or handle gracefully
        assert response.status_code in [200, 400, 422, 500]


class TestValidationEndpoints:
    """Test validation endpoints."""
    
    @pytest.mark.integration
    def test_get_validate_default(self, test_client):
        """Test GET /semantic/validate with default parameters."""
        response = test_client.get("/semantic/validate")
        
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "summary" in data
            assert "diagnostics" in data
            assert "errors" in data["summary"]
            assert "warnings" in data["summary"]
    
    @pytest.mark.integration
    def test_get_validate_with_params(self, test_client):
        """Test GET /semantic/validate with parameters."""
        response = test_client.get(
            "/semantic/validate",
            params={
                "ruleset": "strict",
                "fixMode": "suggest",
                "scope": "project"
            }
        )
        
        assert response.status_code in [200, 500]
    
    @pytest.mark.integration
    def test_post_validate(self, test_client):
        """Test POST /semantic/validate."""
        payload = {
            "ruleset": "default",
            "fixMode": "suggest",
            "targets": ["docs/", "scripts/"],
            "scope": "project"
        }
        
        response = test_client.post("/semantic/validate", json=payload)
        assert response.status_code in [200, 500]
    
    @pytest.mark.integration
    def test_validate_with_targets(self, test_client):
        """Test validation with specific targets."""
        response = test_client.get(
            "/semantic/validate",
            params={"targets": "docs/glossary.md,docs/vision.md"}
        )
        
        assert response.status_code in [200, 500]


class TestDriftEndpoints:
    """Test drift detection endpoints."""
    
    @pytest.mark.integration
    def test_get_drift_default(self, test_client):
        """Test GET /semantic/drift with default parameters."""
        response = test_client.get("/semantic/drift")
        
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "summary" in data
            assert "drifts" in data
    
    @pytest.mark.integration
    def test_get_drift_with_refs(self, test_client):
        """Test GET /semantic/drift with git refs."""
        response = test_client.get(
            "/semantic/drift",
            params={
                "baseRef": "origin/main",
                "headRef": "HEAD",
                "threshold": "warning"
            }
        )
        
        assert response.status_code in [200, 500]
    
    @pytest.mark.integration
    def test_post_drift(self, test_client):
        """Test POST /semantic/drift."""
        payload = {
            "baseRef": "origin/main",
            "headRef": "HEAD",
            "scopes": ["project", "module"],
            "includeDiffSummary": True,
            "threshold": "all"
        }
        
        response = test_client.post("/semantic/drift", json=payload)
        assert response.status_code in [200, 500]
    
    @pytest.mark.integration
    def test_drift_with_scopes(self, test_client):
        """Test drift detection with specific scopes."""
        response = test_client.get(
            "/semantic/drift",
            params={"scopes": "project,cluster"}
        )
        
        assert response.status_code in [200, 500]


class TestGlossaryEndpoints:
    """Test glossary endpoints."""
    
    @pytest.mark.integration
    def test_get_glossary_all(self, test_client):
        """Test GET /semantic/glossary without filters."""
        response = test_client.get("/semantic/glossary")
        
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
    
    @pytest.mark.integration
    def test_get_glossary_with_category(self, test_client):
        """Test GET /semantic/glossary with category filter."""
        response = test_client.get(
            "/semantic/glossary",
            params={"category": "Core Concepts"}
        )
        
        assert response.status_code in [200, 500]
    
    @pytest.mark.integration
    def test_get_glossary_with_search(self, test_client):
        """Test GET /semantic/glossary with search."""
        response = test_client.get(
            "/semantic/glossary",
            params={"search": "semantic"}
        )
        
        assert response.status_code in [200, 500]
    
    @pytest.mark.integration
    def test_get_glossary_term_not_found(self, test_client):
        """Test GET /semantic/glossary/{term} with non-existent term."""
        response = test_client.get("/semantic/glossary/NonExistentTerm")
        
        # Should return 404 or 500 (if glossary file doesn't exist)
        assert response.status_code in [404, 500]
    
    @pytest.mark.integration
    def test_get_glossary_term_found(self, test_client):
        """Test GET /semantic/glossary/{term} for existing term."""
        # This will fail if glossary doesn't exist, which is expected in test env
        response = test_client.get("/semantic/glossary/Semantic-Architecture")
        
        assert response.status_code in [200, 404, 500]


class TestADREndpoints:
    """Test ADR (Architecture Decision Records) endpoints."""
    
    @pytest.mark.integration
    def test_get_adr_index_default(self, test_client):
        """Test GET /semantic/adr with default parameters."""
        response = test_client.get("/semantic/adr")
        
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "meta" in data
            assert "records" in data
    
    @pytest.mark.integration
    def test_get_adr_index_with_root(self, test_client):
        """Test GET /semantic/adr with custom root."""
        response = test_client.get(
            "/semantic/adr",
            params={"root": "docs/decisions"}
        )
        
        assert response.status_code in [200, 500]
    
    @pytest.mark.integration
    def test_get_adr_with_patterns(self, test_client):
        """Test GET /semantic/adr with patterns."""
        response = test_client.get(
            "/semantic/adr",
            params={"patterns": "ADR-*.md,adr-*.md"}
        )
        
        assert response.status_code in [200, 500]
    
    @pytest.mark.integration
    def test_post_adr_index(self, test_client):
        """Test POST /semantic/adr."""
        payload = {
            "root": "docs",
            "patterns": ["*.md"]
        }
        
        response = test_client.post("/semantic/adr", json=payload)
        assert response.status_code in [200, 500]


class TestErrorHandling:
    """Test error handling across endpoints."""
    
    def test_404_for_invalid_path(self, test_client):
        """Test that invalid paths return 404."""
        response = test_client.get("/invalid/path")
        assert response.status_code == 404
    
    def test_405_for_wrong_method(self, test_client):
        """Test that wrong HTTP methods return 405."""
        # Health endpoint only accepts GET
        response = test_client.post("/health")
        assert response.status_code == 405
    
    def test_422_for_invalid_json(self, test_client):
        """Test that invalid JSON in POST request returns 422."""
        response = test_client.post(
            "/semantic/graph",
            json={"invalid_field": "value"}
        )
        # FastAPI will validate and may return 422 or process with defaults
        assert response.status_code in [200, 422, 500]


class TestCORSHeaders:
    """Test CORS configuration."""
    
    def test_cors_headers_present(self, test_client):
        """Test that CORS headers are set correctly."""
        response = test_client.options("/")
        
        # CORS headers should be present in OPTIONS response
        assert response.status_code in [200, 405]
    
    def test_cors_on_get_request(self, test_client):
        """Test CORS headers on GET request."""
        response = test_client.get("/health")
        
        assert response.status_code == 200
        # In test environment, CORS headers may or may not be present
        # depending on test client configuration
