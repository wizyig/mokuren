from __future__ import annotations
import json
from pathlib import Path
from converter.validator import CHECKS

def _load(path):
    text = Path(path).read_text(encoding="utf-8")
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        return json.loads(text)

def to_dot(data):
    rec_map = {r["node_id"]: r for r in data.get("records", [])}
    lines = ["digraph MOKUREN {", "  rankdir=TB;", "  node [shape=box, fontname=monospace];"]
    for node in data.get("nodes", []):
        nid = node["id"]
        rec = rec_map.get(nid, {})
        checks = rec.get("checks", {})
        pat = " ".join(str(checks.get(c, "0")) for c in CHECKS)
        status = rec.get("status", "")
        label = f"{nid}\\n{node['type']}\\n[{pat}]\\n{status}"
        lines.append(f'  "{nid}" [label="{label}"];')
    for edge in data.get("edges", []):
        lines.append(f'  "{edge["from"]}" -> "{edge["to"]}";')
    lines.append("}")
    return "\n".join(lines) + "\n"
