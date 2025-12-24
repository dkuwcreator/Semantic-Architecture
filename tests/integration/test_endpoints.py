"""Integration tests for repository tooling scripts (non-server).

These tests validate that key scripts execute successfully and emit JSON output.
"""

import pytest

from tests.helpers.script_runner import run_script


class TestToolingScripts:
    @pytest.mark.integration
    def test_semantic_graph_runs_and_emits_json(self):
        result = run_script("semantic_graph.py", ["--outputFormat", "json"])
        assert result.exit_code == 0
        assert isinstance(result.parsed_json, dict)
        assert "nodes" in result.parsed_json
        assert "edges" in result.parsed_json
        assert "meta" in result.parsed_json

    @pytest.mark.integration
    def test_semantic_validator_runs_and_emits_json(self):
        result = run_script("semantic_validator.py", ["--targets", ".", "--ruleset", "default", "--outputFormat", "json"])
        assert result.exit_code in (0, 1)
        assert isinstance(result.parsed_json, dict)
        assert "diagnostics" in result.parsed_json
        assert "summary" in result.parsed_json

    @pytest.mark.integration
    def test_adr_index_runs_and_emits_json(self):
        result = run_script("adr_index.py", ["--root", "docs"])
        assert result.exit_code == 0
        assert isinstance(result.parsed_json, dict)
        assert "records" in result.parsed_json
        assert "meta" in result.parsed_json

    @pytest.mark.integration
    def test_semantic_drift_scanner_runs_and_emits_json(self):
        # In environments without an upstream ref (origin/main), the script should still handle errors gracefully.
        result = run_script("semantic_drift_scanner.py", ["--baseRef", "origin/main", "--headRef", "HEAD"])
        assert result.exit_code == 0
        assert isinstance(result.parsed_json, dict)
        assert "drifts" in result.parsed_json
        assert "summary" in result.parsed_json
