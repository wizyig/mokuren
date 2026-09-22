"""Stable MGF I/O.

    load_csv / load_yaml / dump_yaml / dump_csv / core_snapshot
"""
from __future__ import annotations
import csv, io
from pathlib import Path
from converter.csv_to_yaml import csv_to_mgf, dump_yaml as _dump_yaml_text
from converter.validator import CHECKS
from converter.yaml_to_csv import HEADER, _load as _load_yaml, yaml_to_rows

def load_csv(path, dataset_type="observed", sample_data=False):
    return csv_to_mgf(str(path), dataset_type=dataset_type, sample_data=sample_data)

def load_yaml(path):
    return _load_yaml(str(path))

def dump_yaml(data, path=None):
    text = _dump_yaml_text(data)
    if path is not None:
        Path(path).write_text(text, encoding="utf-8")
    return text

def dump_csv(data, path=None):
    rows = yaml_to_rows(data)
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=HEADER, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    text = buf.getvalue()
    if path is not None:
        Path(path).write_text(text, encoding="utf-8")
    return text

def core_snapshot(data):
    run = data.get("run") or {}
    records = []
    for rec in data.get("records") or []:
        checks = rec.get("checks") or {}
        records.append({
            "record_id": str(rec.get("record_id", "")),
            "node_id": str(rec.get("node_id", "")),
            "source_id": str(rec.get("source_id", "")),
            "observed_date": str(rec.get("observed_date", "")),
            "status": str(rec.get("status", "")),
            "notes": str(rec.get("notes", "")),
            "checks": {c: str(checks.get(c, "0")) for c in CHECKS},
        })
    return {
        "mgf_version": str(data.get("mgf_version", "")),
        "run_id": str(run.get("run_id", "")),
        "nodes": sorted([{"id": n["id"], "type": n["type"]} for n in data.get("nodes") or []], key=lambda x: x["id"]),
        "edges": sorted([{"from": e["from"], "to": e["to"]} for e in data.get("edges") or []], key=lambda x: (x["from"], x["to"])),
        "records": records,
    }
