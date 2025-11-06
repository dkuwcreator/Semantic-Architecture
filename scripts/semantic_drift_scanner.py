#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from typing import Any, Dict, List


def parse_args():
    p = argparse.ArgumentParser(description="Detect semantic drift across git refs")
    p.add_argument("--baseRef", default="origin/main")
    p.add_argument("--headRef", default="HEAD")
    p.add_argument("--scopes", nargs="*", default=None)
    p.add_argument("--includeDiffSummary", action="store_true", default=True)
    p.add_argument("--threshold", choices=["all", "error", "warning"], default="all")
    return p.parse_args()


def git_diff_names(base: str, head: str) -> List[str]:
    try:
        out = subprocess.check_output(["git", "diff", "--name-only", base, head], stderr=subprocess.STDOUT, text=True)
        return [line.strip() for line in out.splitlines() if line.strip()]
    except Exception:
        return []


def classify_drift(files: List[str]) -> List[Dict[str, Any]]:
    drifts: List[Dict[str, Any]] = []
    for f in files:
        scope = "module" if os.path.basename(f).lower() in ("semantic-instructions.md", "about.md") else "module"
        drift_type = None
        if f.lower().endswith("semantic-instructions.md"):
            drift_type = "contract-changed"
        elif f.lower().endswith("about.md"):
            drift_type = "doc-missing"
        elif f.lower().endswith(".py") or f.lower().endswith(".ts"):
            drift_type = "code-changed"
        else:
            continue
        # short diagnostic codes
        code_map = {
            "contract-changed": "DR001",
            "doc-missing": "DR002",
            "code-changed": "DR003",
        }
        drifts.append({
            "code": code_map.get(drift_type, "DR000"),
            "id": f,
            "type": drift_type,
            "scope": scope,
            "target": {"id": f, "path": f},
            "message": f"Change detected in {f}",
            "confidence": 0.5 if drift_type != "contract-changed" else 0.8,
        })
    return drifts


def main() -> int:
    args = parse_args()
    changed = git_diff_names(args.baseRef, args.headRef)
    drifts = classify_drift(changed)

    summary = {"count": len(drifts), "byType": {}, "bySeverity": {}}
    for d in drifts:
        summary["byType"][d["type"]] = summary["byType"].get(d["type"], 0) + 1

    out = {
        "drifts": drifts,
        "summary": summary,
        "diffSummary": "\n".join(changed) if args.includeDiffSummary else "",
        "meta": {
            "generatedAt": datetime.utcnow().isoformat() + "Z",
            "toolVersion": "0.1.0",
            "baseRef": args.baseRef,
            "headRef": args.headRef,
        },
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
