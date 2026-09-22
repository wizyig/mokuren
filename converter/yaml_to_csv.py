from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from converter.validator import CHECKS
HEADER = ["run_id","record_id","node_id","node_type","parent_node","next_node","source_id","observed_date","A01","A02","A03","A04","A05","status","notes"]

def _load(path):
    text = Path(path).read_text(encoding="utf-8")
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        return json.loads(text)

def yaml_to_rows(data):
    node_type = {n["id"]: n["type"] for n in data.get("nodes", [])}
    incoming, outgoing = {}, {}
    for e in data.get("edges", []):
        incoming[e["to"]] = e["from"]
        outgoing[e["from"]] = e["to"]
    run_id = data["run"]["run_id"]
    rows = []
    for rec in data.get("records", []):
        nid = rec["node_id"]
        checks = rec.get("checks", {})
        rows.append({
            "run_id": run_id,
            "record_id": rec["record_id"],
            "node_id": nid,
            "node_type": node_type.get(nid, ""),
            "parent_node": incoming.get(nid, ""),
            "next_node": outgoing.get(nid, ""),
            "source_id": rec.get("source_id", ""),
            "observed_date": rec.get("observed_date", ""),
            "A01": checks.get("A01", "0"),
            "A02": checks.get("A02", "0"),
            "A03": checks.get("A03", "0"),
            "A04": checks.get("A04", "0"),
            "A05": checks.get("A05", "0"),
            "status": rec.get("status", ""),
            "notes": rec.get("notes", ""),
        })
    return rows
