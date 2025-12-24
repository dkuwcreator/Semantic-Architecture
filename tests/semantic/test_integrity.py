"""Semantic integrity tests (non-server).

These tests focus on JSON-serializability and minimal semantic guarantees.
"""

import json
from pathlib import Path

import pytest

from tests.helpers.script_runner import run_script


class TestCrossEnvironmentConsistency:
    @pytest.mark.semantic
    def test_mock_outputs_are_json_serializable(self, mock_semantic_graph_output, mock_validation_output, mock_drift_output):
        outputs = [mock_semantic_graph_output, mock_validation_output, mock_drift_output]
        for output in outputs:
            json_str = json.dumps(output)
            parsed = json.loads(json_str)
            assert parsed == output

    @pytest.mark.semantic
    def test_script_outputs_are_json_serializable(self, temp_repo_dir: Path):
        graph = run_script("semantic_graph.py", ["--outputFormat", "json"], workdir=temp_repo_dir)
        assert graph.exit_code == 0
        json.dumps(graph.parsed_json)

        validator = run_script(
            "semantic_validator.py",
            ["--targets", ".", "--ruleset", "default", "--outputFormat", "json"],
            workdir=temp_repo_dir,
        )
        assert validator.exit_code in (0, 1)
        json.dumps(validator.parsed_json)
