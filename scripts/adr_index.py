#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime
from glob import glob
from typing import Any, Dict, List


def parse_args():
    p = argparse.ArgumentParser(description="Index ADR/decision records")
    p.add_argument("--root", default="docs")
    p.add_argument("--patterns", nargs="*", default=["**/adr-*.md", "**/ADR-*.md", "**/decisions/*.md"])
    return p.parse_args()


def index_records(root: str, patterns: List[str]) -> List[Dict[str, Any]]:
    recs: List[Dict[str, Any]] = []
    for pat in patterns:
        for path in glob(os.path.join(root, pat), recursive=True):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    first = f.readline().strip()
                title = os.path.basename(path)
                if first.startswith("# "):
                    title = first.lstrip("# ").strip()
                recs.append({
                    "id": os.path.splitext(os.path.basename(path))[0],
                    "title": title,
                    "path": path.replace("\\", "/"),
                })
            except Exception:
                recs.append({"id": os.path.basename(path), "title": os.path.basename(path), "path": path.replace("\\", "/")})
    return sorted(recs, key=lambda r: r["path"])


def main() -> int:
    args = parse_args()
    records = index_records(args.root, args.patterns)
    out = {
        "records": records,
        "meta": {"generatedAt": datetime.utcnow().isoformat() + "Z", "count": len(records)}
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
