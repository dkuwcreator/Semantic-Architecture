"""Illustrative, NON-NORMATIVE code stub.

This file exists only to demonstrate meaning-first parity (docs ↔ behavior).
The normative rules for Semantic Architecture are in docs/core-spec.md.
"""

from __future__ import annotations

from pathlib import Path
import importlib.util


def _import_alpha_greet() -> callable:
    alpha_path = Path(__file__).parent.parent / "module-alpha" / "stub.py"
    spec = importlib.util.spec_from_file_location("module_alpha_stub", alpha_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load module-alpha stub")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "greet")


def greet_from_alpha(name: str) -> str:
    greet = _import_alpha_greet()
    return greet(name)


if __name__ == "__main__":
    print(greet_from_alpha("World"))
