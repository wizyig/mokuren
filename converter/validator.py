"""MGF CSV / YAML structural validator. Fail-closed. No scoring."""
from __future__ import annotations
import csv, json, re
from datetime import datetime
from pathlib import Path
CHECKS = ("A01", "A02", "A03", "A04", "A05")
ALLOWED_CHECK = {"Y", "N", "0"}
NODE_TYPES = {"input", "observed", "candidate", "review"}
STATUS_VALUES = {"active", "observed", "candidate", "pending", "closed"}
DATASET_TYPES = {"observed", "sample", "synthetic"}
RUN_ID = re.compile(r"^\\d{8}-\\d{3}$")
NODE_ID = re.compile(r"^[a-z0-9_\\-]+$")
CSV_REQUIRED = ("run_id", "record_id", "node_id", "node_type", "observed_date", "A01", "A02", "A03", "A04", "A05", "status")
DEFAULT_CHECKS = [
    {"id": "A01", "name": "evidence_present"},
    {"id": "A02", "name": "reproducible"},
    {"id": "A03", "name": "history_available"},
    {"id": "A04", "name": "source_identified"},
    {"id": "A05", "name": "review_required"},
]

def validate_date(value):
    try:
        datetime.strptime(str(value), "%Y-%m-%d")
        return True
    except ValueError:
        return False

def detect_duplicates(rows):
    seen, dups = set(), []
    for row in rows:
        key = (str(row.get("record_id", "")), str(row.get("node_id", "")))
        if key in seen:
            dups.append(key)
        else:
            seen.add(key)
    return dups

def validate_csv(path):
    errors = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return ["missing_header"]
        cols = list(reader.fieldnames)
        for col in CSV_REQUIRED:
            if col not in cols:
                errors.append(f"missing_column:{col}")
        if errors:
            return errors
        rows = list(reader)
    for idx, row in enumerate(rows, start=2):
        rid = str(row.get("run_id", "")).strip()
        if not RUN_ID.match(rid):
            errors.append(f"line={idx} invalid_run_id={rid}")
        ntype = str(row.get("node_type", "")).strip()
        if ntype not in NODE_TYPES:
            errors.append(f"line={idx} invalid_node_type={ntype}")
        status = str(row.get("status", "")).strip()
        if status not in STATUS_VALUES:
            errors.append(f"line={idx} invalid_status={status}")
        if not validate_date(row.get("observed_date", "")):
            errors.append(f"line={idx} invalid_date={row.get('observed_date')}")
        nid = str(row.get("node_id", "")).strip()
        if not nid or not NODE_ID.match(nid):
            errors.append(f"line={idx} invalid_node_id={nid}")
        for c in CHECKS:
            value = str(row.get(c, "")).strip()
            if value not in ALLOWED_CHECK:
                errors.append(f"line={idx} invalid_check {c}={value}")
    for record_id, node_id in detect_duplicates(rows):
        errors.append(f"duplicate:{record_id}/{node_id}")
    return errors

def _load_yaml(path):
    text = Path(path).read_text(encoding="utf-8")
    try:
        import yaml
        data = yaml.safe_load(text)
    except ImportError:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("root must be object")
    return data

def validate_yaml(path):
    errors = []
    try:
        data = _load_yaml(path)
    except Exception as exc:
        return [f"parse_error:{exc}"]
    if data.get("mgf_version") != "1.0":
        errors.append(f"invalid_mgf_version={data.get('mgf_version')}")
    extra_top = set(data) - {"mgf_version", "run", "checks", "nodes", "edges", "records"}
    for k in extra_top:
        errors.append(f"extra_property:{k}")
    for key in ("mgf_version", "run", "nodes", "edges", "records"):
        if key not in data:
            errors.append(f"missing:{key}")
    run = data.get("run") or {}
    if not isinstance(run, dict):
        errors.append("invalid_run")
        return errors
    if not RUN_ID.match(str(run.get("run_id", ""))):
        errors.append(f"invalid_run_id={run.get('run_id')}")
    if run.get("dataset_type") not in DATASET_TYPES:
        errors.append(f"invalid_dataset_type={run.get('dataset_type')}")
    if not isinstance(run.get("sample_data"), bool):
        errors.append("invalid_sample_data")
    node_ids = set()
    for node in data.get("nodes") or []:
        nid = str(node.get("id", ""))
        if not NODE_ID.match(nid):
            errors.append(f"invalid_node_id={nid}")
        if node.get("type") not in NODE_TYPES:
            errors.append(f"invalid_node_type={node.get('type')}")
        node_ids.add(nid)
    for edge in data.get("edges") or []:
        if edge.get("from") not in node_ids:
            errors.append(f"orphan_edge_from={edge.get('from')}")
        if edge.get("to") not in node_ids:
            errors.append(f"orphan_edge_to={edge.get('to')}")
    seen = set()
    for rec in data.get("records") or []:
        checks = rec.get("checks") or {}
        for c in CHECKS:
            v = str(checks.get(c, ""))
            if v not in ALLOWED_CHECK:
                errors.append(f"invalid_check {rec.get('record_id')}/{c}={v}")
        if rec.get("status") is not None and rec.get("status") not in STATUS_VALUES:
            errors.append(f"invalid_status={rec.get('status')}")
        key = (str(rec.get("record_id")), str(rec.get("node_id")))
        if key in seen:
            errors.append(f"duplicate:{key[0]}/{key[1]}")
        seen.add(key)
    return errors
