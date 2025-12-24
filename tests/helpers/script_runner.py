from __future__ import annotations

import io
import json
import os
import runpy
import sys
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]


class ScriptRunError(RuntimeError):
    pass


@dataclass(frozen=True)
class ScriptResult:
    exit_code: int
    stdout: str
    stderr: str
    parsed_json: Any | None


def _validate_script_name(script_name: str) -> None:
    if not script_name or script_name.strip() != script_name:
        raise ScriptRunError("Invalid script name")

    # Only allow plain filenames (no directories) to avoid traversal.
    if "/" in script_name or "\\" in script_name:
        raise ScriptRunError("Invalid script name (path traversal)")

    if not script_name.endswith(".py"):
        raise ScriptRunError("Invalid script name (must be .py)")


def run_script(
    script_name: str,
    args: Sequence[str] | None = None,
    *,
    repo_root: Path | None = None,
    workdir: Path | None = None,
    expect_json: bool = True,
) -> ScriptResult:
    """Run a repo script in-process (coverage-friendly) and capture stdout/stderr.

    - `script_name` is a filename under `<repo_root>/scripts/`.
    - `workdir` controls the current working directory during execution.

    Returns a ScriptResult with exit code and captured output.
    """

    _validate_script_name(script_name)
    script_args = list(args or [])

    repo_root = repo_root or REPO_ROOT
    workdir = workdir or repo_root

    script_path = (repo_root / "scripts" / script_name).resolve()
    if not script_path.is_file():
        raise ScriptRunError(f"Script not found: {script_path}")

    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    old_argv = sys.argv
    old_cwd = os.getcwd()

    exit_code = 0
    try:
        os.chdir(str(workdir))
        sys.argv = [str(script_path)] + script_args
        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            try:
                runpy.run_path(str(script_path), run_name="__main__")
            except SystemExit as e:
                if e.code is None:
                    exit_code = 0
                elif isinstance(e.code, int):
                    exit_code = e.code
                else:
                    exit_code = 1
    except Exception as e:
        stderr_buf.write(f"\n{type(e).__name__}: {e}\n")
        raise ScriptRunError(f"Failed to run {script_name}") from e
    finally:
        sys.argv = old_argv
        os.chdir(old_cwd)

    stdout = stdout_buf.getvalue().strip()
    stderr = stderr_buf.getvalue().strip()

    parsed: Any | None = None
    if expect_json:
        try:
            parsed = json.loads(stdout) if stdout else None
        except json.JSONDecodeError as e:
            raise ScriptRunError(f"Failed to parse JSON output from {script_name}: {e}") from e

    return ScriptResult(exit_code=exit_code, stdout=stdout, stderr=stderr, parsed_json=parsed)
