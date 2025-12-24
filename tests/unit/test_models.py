"""Unit tests for script output shapes (non-server).

These tests validate that scripts emit stable, JSON-serializable structures.
"""

import json
from pathlib import Path

import pytest

from tests.helpers.script_runner import run_script


class TestScriptOutputShapes:
    @pytest.mark.unit
    def test_semantic_graph_output_shape_in_temp_repo(self, temp_repo_dir: Path):
        result = run_script("semantic_graph.py", ["--outputFormat", "json"], workdir=temp_repo_dir)
        assert result.exit_code == 0
        assert isinstance(result.parsed_json, dict)
        assert isinstance(result.parsed_json.get("nodes"), list)
        assert isinstance(result.parsed_json.get("edges"), list)
        assert isinstance(result.parsed_json.get("meta"), dict)

        # Always includes a project root node.
        assert len(result.parsed_json["nodes"]) >= 1
        assert result.parsed_json["nodes"][0]["scope"] == "project"

    @pytest.mark.unit
    def test_semantic_validator_reports_error_for_missing_front_matter(self, temp_repo_dir: Path):
        module_dir = temp_repo_dir / "module-a"
        module_dir.mkdir(parents=True, exist_ok=True)

        si_path = module_dir / "semantic-instructions.md"
        si_path.write_text("# no front matter\n\ncontent\n", encoding="utf-8")

        result = run_script(
            "semantic_validator.py",
            ["--targets", ".", "--ruleset", "default", "--outputFormat", "json"],
            workdir=temp_repo_dir,
        )

        assert result.exit_code == 1
        assert isinstance(result.parsed_json, dict)
        assert "diagnostics" in result.parsed_json
        assert result.parsed_json["summary"]["errors"] >= 1

    @pytest.mark.unit
    def test_adr_index_output_is_json_serializable(self, temp_repo_dir: Path):
        result = run_script("adr_index.py", ["--root", "docs"], workdir=temp_repo_dir)
        assert result.exit_code == 0
        json.dumps(result.parsed_json)

    @pytest.mark.unit
    def test_drift_scanner_output_has_expected_keys(self, temp_repo_dir: Path):
        result = run_script(
            "semantic_drift_scanner.py",
            ["--baseRef", "origin/main", "--headRef", "HEAD"],
            workdir=temp_repo_dir,
        )
        assert result.exit_code == 0
        assert isinstance(result.parsed_json, dict)
        assert "drifts" in result.parsed_json
        assert "summary" in result.parsed_json
        assert "meta" in result.parsed_json
