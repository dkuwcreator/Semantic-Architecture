#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Emit semantic graph from repository")
    p.add_argument("--scope", choices=["project", "cluster", "module"], default="project")
    p.add_argument("--ids", nargs="*", default=None)
    p.add_argument("--include", nargs="*", default=None)
    p.add_argument("--edgeTypes", nargs="*", default=None)
    p.add_argument("--outputFormat", choices=["json", "dot"], default="json")
    p.add_argument("--filters", default=None, help="JSON object with filters")
    p.add_argument("--version", default="0.1")
    return p.parse_args()


def read_project_owners(repo_root: str) -> List[str]:
    owners: List[str] = []
    governance = os.path.join(repo_root, ".github", "copilot-instructions.md")
    if os.path.isfile(governance):
        try:
            with open(governance, "r", encoding="utf-8") as f:
                txt = f.read()
            # Read YAML front matter owners: ["@handle"]
            fm = None
            if txt.startswith("---"):
                parts = txt.split("---", 2)
                if len(parts) >= 3:
                    fm = parts[1]
            if fm:
                m = re.search(r"owners:\s*\[(.*?)\]", fm)
                if m:
                    raw = m.group(1)
                    owners = [s.strip().strip('"\'') for s in raw.split(";") for s in s.split(",") if s.strip()]
        except Exception:
            pass
    return owners


def find_semantic_instruction_files(repo_root: str) -> List[str]:
    matches: List[str] = []
    for root, _dirs, files in os.walk(repo_root):
        for fn in files:
            if fn.lower() == "semantic-instructions.md":
                matches.append(os.path.join(root, fn))
    return matches


def build_graph(repo_root: str, scope: str, ids: List[str] | None) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    owners = read_project_owners(repo_root)
    project_id = os.path.basename(repo_root.rstrip(os.sep)) or "project"

    # Always include a project node as root
    nodes.append({
        "id": f"project:{project_id}",
        "scope": "project",
        "name": project_id,
        "path": ".",
        "owners": owners,
        "contract": {"invariants": [], "validation": {"tests": []}},
        "meta": {"detected": True}
    })

    # Discover modules by presence of semantic-instructions.md
    for path in find_semantic_instruction_files(repo_root):
        rel = os.path.relpath(path, repo_root)
        module_id = rel.replace(os.sep, "/").rsplit("/", 1)[0]
        node = {
            "id": f"module:{module_id}",
            "scope": "module",
            "name": os.path.basename(module_id),
            "path": module_id,
            "owners": [],
            "contract": {"invariants": [], "validation": {"tests": []}},
        }
        nodes.append(node)
        edges.append({"from": f"project:{project_id}", "to": node["id"], "type": "contains"})

    # Scope filtering
    if ids:
        idset = set(ids)
        nodes = [n for n in nodes if n.get("id") in idset or n.get("path") in idset]
        # Keep edges only if both ends remain
        keep = {n["id"] for n in nodes}
        edges = [e for e in edges if e.get("from") in keep and e.get("to") in keep]

    return {
        "nodes": nodes,
        "edges": edges,
        "meta": {
            "generatedAt": datetime.utcnow().isoformat() + "Z",
            "toolVersion": "0.1.0",
        }
    }


def to_dot(graph: Dict[str, Any]) -> str:
    lines = ["digraph SemanticGraph {"]
    for n in graph["nodes"]:
        nid = n["id"].replace("\"", "'")
        label = n.get("name", n["id"]).replace("\"", "'")
        lines.append(f'  "{nid}" [label="{label}"];')
    for e in graph["edges"]:
        a = e["from"].replace("\"", "'")
        b = e["to"].replace("\"", "'")
        et = e.get("type", "rel")
        lines.append(f'  "{a}" -> "{b}" [label="{et}"];')
    lines.append("}")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    repo_root = os.getcwd()

    # Parse filters if provided (but not applied in stub)
    try:
        _filters = json.loads(args.filters) if args.filters else None
    except json.JSONDecodeError:
        _filters = None

    graph = build_graph(repo_root, args.scope, args.ids)

    if args.outputFormat == "dot":
        print(to_dot(graph))
    else:
        print(json.dumps(graph, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
