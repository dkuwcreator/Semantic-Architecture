#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from datetime import datetime
from glob import glob
from typing import Any, Dict, List


SEVERITY = ("error", "warning", "info")


def parse_args():
    p = argparse.ArgumentParser(description="Validate semantic files and contracts")
    p.add_argument("--targets", nargs="*", default=["."])
    p.add_argument("--scope", choices=["project", "cluster", "module"], default=None)
    p.add_argument("--ruleset", choices=["default", "strict", "ci"], default="default")
    p.add_argument("--fixMode", choices=["none", "suggest"], default="suggest")
    p.add_argument("--outputFormat", choices=["json"], default="json")
    return p.parse_args()


def add_diag(diags: List[Dict[str, Any]], severity: str, code: str, message: str, file: str, start: int | None = None, end: int | None = None):
    diags.append({
        "severity": severity,
        "code": code,
        "message": message,
        "location": {"file": file, **({"startLine": start} if start is not None else {}), **({"endLine": end} if end is not None else {})}
    })


def validate_semantic_instructions_md(path: str, diags: List[Dict[str, Any]]):
    try:
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        if not txt.startswith("---"):
            add_diag(diags, "error", "SI001", "Missing YAML front matter", path, 1, 1)
            return
        parts = txt.split("---", 2)
        fm = parts[1]
        # required: scope, id, owners
        missing = []
        if not re.search(r"\bscope:\s*(project|cluster|module)\b", fm):
            missing.append("scope")
        if not re.search(r"\bid:\s*\S+", fm):
            missing.append("id")
        if not re.search(r"\bowners:\s*\[.*?\]", fm, re.S):
            missing.append("owners")
        for m in missing:
            add_diag(diags, "error", "SI002", f"Missing required field '{m}' in front matter", path, 1, 1)
        
        # Check if this is a module scope
        scope_match = re.search(r"\bscope:\s*(project|cluster|module)\b", fm)
        if scope_match and scope_match.group(1) == "module":
            # Validate module directory structure (one level of subdirectories allowed)
            validate_module_structure(path, diags)
    except Exception as e:
        add_diag(diags, "error", "SI000", f"Failed to read: {e}", path)


def validate_module_structure(semantic_instructions_path: str, diags: List[Dict[str, Any]]):
    """Validate that module directory structure adheres to one-level subdirectory rule."""
    module_dir = os.path.dirname(semantic_instructions_path)
    
    # Walk the module directory and check for nesting depth
    for root, dirs, files in os.walk(module_dir):
        rel_path = os.path.relpath(root, module_dir)
        
        # Skip the module root itself
        if rel_path == ".":
            continue
        
        # Count the depth: one level means one path separator
        depth = rel_path.count(os.sep) + 1
        
        if depth > 1:
            add_diag(
                diags, 
                "error", 
                "SI003", 
                f"Module directory structure exceeds one level of nesting: {rel_path}. Modules may only contain one level of subdirectories.",
                semantic_instructions_path
            )
            # Report only once per module
            break



def collect_targets(inputs: List[str]) -> List[str]:
    results: List[str] = []
    for t in inputs:
        if os.path.isdir(t):
            for root, _dirs, files in os.walk(t):
                for fn in files:
                    if fn.lower() == "semantic-instructions.md":
                        results.append(os.path.join(root, fn))
        else:
            results.extend(glob(t, recursive=True))
    # de-dup
    return sorted(set(results))


def main() -> int:
    args = parse_args()
    diags: List[Dict[str, Any]] = []

    # CI/strict may enforce presence of core docs
    if args.ruleset in ("ci", "strict"):
        required = [
            os.path.join("docs", "vision.md"),
            os.path.join("docs", "semantic-project-model.md"),
            os.path.join("docs", "semantic-collaboration-model.md"),
            os.path.join("docs", "glossary.md"),
        ]
        for f in required:
            if not os.path.isfile(f):
                add_diag(diags, "error", "DOC001", f"Required document missing: {f}", f)

    target_files = collect_targets(args.targets)
    for path in target_files:
        validate_semantic_instructions_md(path, diags)

    summary = {
        "errors": sum(1 for d in diags if d["severity"] == "error"),
        "warnings": sum(1 for d in diags if d["severity"] == "warning"),
        "infos": sum(1 for d in diags if d["severity"] == "info"),
        "ruleset": args.ruleset,
        "scope": args.scope or "auto",
    }
    out = {"diagnostics": diags, "summary": summary, "meta": {"generatedAt": datetime.utcnow().isoformat() + "Z", "toolVersion": "0.1.0", "schemaVersion": "1"}}
    print(json.dumps(out, indent=2))

    return 1 if summary["errors"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
