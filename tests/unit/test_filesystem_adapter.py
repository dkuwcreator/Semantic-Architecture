"""Unit tests for the script runner helper (replacing server filesystem adapter tests).

The repository no longer ships a server runtime; tests validate safe script invocation.
"""

from pathlib import Path

import pytest

from tests.helpers.script_runner import ScriptRunError, run_script


class TestScriptRunner:
    @pytest.mark.unit
    def test_rejects_empty_script_name(self):
        with pytest.raises(ScriptRunError, match="Invalid script name"):
            run_script("")

    @pytest.mark.unit
    def test_rejects_path_traversal(self):
        with pytest.raises(ScriptRunError, match="path traversal"):
            run_script("../etc/passwd")

        with pytest.raises(ScriptRunError, match="path traversal"):
            run_script("..\\etc\\passwd")

    @pytest.mark.unit
    def test_requires_py_extension(self):
        with pytest.raises(ScriptRunError, match="must be \\.py"):
            run_script("semantic_graph")

    @pytest.mark.unit
    def test_raises_on_non_json_output_when_expected(self):
        # semantic_graph can emit DOT; ensure we fail parsing when expect_json=True.
        with pytest.raises(ScriptRunError, match="Failed to parse JSON"):
            run_script("semantic_graph.py", ["--outputFormat", "dot"], expect_json=True)

    @pytest.mark.unit
    def test_can_run_in_temp_workdir(self, temp_repo_dir: Path):
        result = run_script("semantic_graph.py", ["--outputFormat", "json"], workdir=temp_repo_dir)
        assert result.exit_code == 0
        assert isinstance(result.parsed_json, dict)
