"""Pytest configuration and shared fixtures for Semantic Architecture (non-server).

This module provides common fixtures used across unit, integration, and semantic tests.
It sets up mock data and temporary repository structures.
"""
import os
import pytest
import tempfile
from pathlib import Path
from typing import Generator, Dict, Any


@pytest.fixture
def temp_repo_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory simulating a repository structure.
    
    Yields:
        Path: Path to temporary repository directory
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        
        # Create basic directory structure
        (repo_path / "scripts").mkdir()
        (repo_path / "docs").mkdir()
        (repo_path / "data").mkdir()
        (repo_path / ".github").mkdir()
        
        yield repo_path


@pytest.fixture
def mock_glossary_file(temp_repo_dir: Path) -> Path:
    """Create a mock glossary file for testing.
    
    Args:
        temp_repo_dir: Temporary repository directory
        
    Returns:
        Path: Path to the mock glossary file
    """
    glossary_path = temp_repo_dir / "docs" / "glossary.md"
    glossary_content = """# Glossary

## Core Concepts

### Semantic Architecture
A framework for organizing code using semantic context and meaning.

### Module
A bounded context with specific responsibilities and clear interfaces.

## Development Practices

### Test-Driven Development
Writing tests before implementation code to ensure requirements are met.
"""
    glossary_path.write_text(glossary_content)
    return glossary_path


@pytest.fixture
def mock_semantic_graph_output() -> Dict[str, Any]:
    """Provide mock semantic graph output for testing.
    
    Returns:
        Dict: Mock semantic graph data
    """
    return {
        "nodes": [
            {
                "id": "module-core",
                "scope": "module",
                "name": "Core Module",
                "path": "/modules/core",
                "owners": ["@team-core"],
                "contract": {
                    "invariants": ["must have tests"],
                    "validation": {}
                },
                "meta": {
                    "description": "Core functionality"
                }
            },
            {
                "id": "module-api",
                "scope": "module",
                "name": "API Module",
                "path": "/modules/api",
                "owners": ["@team-api"],
                "contract": {
                    "invariants": [],
                    "validation": {}
                },
                "meta": {
                    "description": "API endpoints"
                }
            }
        ],
        "edges": [
            {
                "from": "module-api",
                "to": "module-core",
                "type": "depends-on",
                "label": "uses",
                "confidence": 0.95
            }
        ],
        "meta": {
            "generatedAt": "2025-11-06T19:00:00Z",
            "toolVersion": "1.0.0",
            "projectVersion": "0.1.0"
        }
    }


@pytest.fixture
def mock_validation_output() -> Dict[str, Any]:
    """Provide mock validation result output for testing.
    
    Returns:
        Dict: Mock validation result data
    """
    return {
        "diagnostics": [
            {
                "severity": "warning",
                "code": "missing-steward",
                "message": "Missing steward field in semantic instructions",
                "location": {
                    "file": "docs/semantic-instructions.md",
                    "startLine": 10,
                    "endLine": 10
                },
                "related": [],
                "suggestedFix": {
                    "patchFormat": "unified",
                    "patch": "+steward: @team-core"
                }
            }
        ],
        "summary": {
            "errors": 0,
            "warnings": 1,
            "infos": 0,
            "ruleset": "default",
            "scope": "project"
        },
        "meta": {
            "generatedAt": "2025-11-06T19:00:00Z",
            "toolVersion": "1.0.0",
            "schemaVersion": "1"
        }
    }


@pytest.fixture
def mock_drift_output() -> Dict[str, Any]:
    """Provide mock drift report output for testing.
    
    Returns:
        Dict: Mock drift report data
    """
    return {
        "drifts": [
            {
                "code": "boundary-change",
                "id": "drift-001",
                "type": "structural",
                "scope": "module",
                "target": {
                    "id": "module-core",
                    "path": "module-core/semantic-instructions.md"
                },
                "message": "Module boundary changed",
                "confidence": 0.9
            },
            {
                "code": "glossary-update",
                "id": "drift-002",
                "type": "semantic",
                "scope": "project",
                "target": {
                    "id": "glossary",
                    "path": "docs/glossary.md"
                },
                "message": "Glossary term updated",
                "confidence": 0.85
            }
        ],
        "summary": {
            "count": 2,
            "byType": {
                "structural": 1,
                "semantic": 1
            },
            "bySeverity": {
                "warning": 1,
                "info": 1
            }
        },
        "diffSummary": "2 files changed, 5 insertions(+), 3 deletions(-)",
        "meta": {
            "generatedAt": "2025-11-06T19:00:00Z",
            "toolVersion": "1.0.0",
            "baseRef": "origin/main",
            "headRef": "HEAD"
        }
    }


@pytest.fixture
def mock_adr_output() -> Dict[str, Any]:
    """Provide mock ADR index output for testing.
    
    Returns:
        Dict: Mock ADR index data
    """
    return {
        "records": [
            {
                "id": "ADR-001",
                "title": "Remove MCP Server Deliverable",
                "path": "docs/decisions/001-remove-mcp-server.md"
            },
            {
                "id": "ADR-002",
                "title": "Adopt Semantic Architecture",
                "path": "docs/decisions/002-semantic-architecture.md"
            }
        ],
        "meta": {
            "generatedAt": "2025-11-06T19:00:00Z",
            "count": 2
        }
    }


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables before and after each test.
    
    This fixture automatically runs for all tests to ensure clean state.
    """
    # Save original environment
    original_env = os.environ.copy()
    
    # Set test environment variables
    os.environ["TESTING"] = "true"
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_glossary_entries():
    """Provide sample glossary entries for testing.
    
    Returns:
        List: Sample glossary entry data
    """
    return [
        {
            "term": "Semantic Architecture",
            "definition": "A framework for organizing code using semantic context.",
            "category": "Core Concepts"
        },
        {
            "term": "Module",
            "definition": "A bounded context with specific responsibilities.",
            "category": "Core Concepts"
        },
        {
            "term": "Test-Driven Development",
            "definition": "Writing tests before implementation code.",
            "category": "Development Practices"
        }
    ]
