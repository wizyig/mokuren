from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from converter.validator import DEFAULT_CHECKS, CHECKS

def csv_to_mgf(path, dataset_type="observed", sample_data=False):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("empty csv")
    nodes, edges, records, seen_edges = {}, [], [], set()
    for row in rows:
        nid = str(row["node_id"]).strip()
        nodes[nid] = {"id": nid, "type": str(row["node_type"]).strip()}
        nxt = str(row.get("next_node") or row.get("next_node_id") or "").strip()
        if nxt and (nid, nxt) not in seen_edges:
            edges.append({"from": nid, "to": nxt})
            seen_edges.add((nid, nxt))
        records.append({
            "record_id": str(row["record_id"]).strip(),
            "node_id": nid,
            "source_id": str(row.get("source_id") or "").strip(),
            "observed_date": str(row.get("observed_date") or "").strip(),
            "checks": {c: str(row[c]).strip() for c in CHECKS},
            "status": str(row.get("status") or "").strip(),
            "notes": str(row.get("notes") or ""),
        })
    return {
        "mgf_version": "1.0",
        "run": {"run_id": str(rows[0]["run_id"]).strip(), "dataset_type": dataset_type, "sample_data": sample_data},
        "checks": DEFAULT_CHECKS,
        "nodes": list(nodes.values()),
        "edges": edges,
        "records": records,
    }

def dump_yaml(data):
    try:
        import yaml
        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    except ImportError:
        return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
