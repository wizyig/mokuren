#!/usr/bin/env python3
"""Validate MOKUREN observed CSV. No scoring. Fail-closed on unknown values."""

from __future__ import annotations

import argparse
import csv
import re
import sys

RUN_ID = re.compile(r"^\d{8}-\d{3}$")
CHECKS = ("A01", "A02", "A03", "A04", "A05")
ALLOWED_CHECK = {"Y", "N", "0"}
ALLOWED_NODE_TYPE = {"input", "observed", "candidate", "review"}
ALLOWED_STATUS = {"active", "observed", "candidate", "pending", "closed"}
REQUIRED = (
    "run_id",
    "record_id",
    "node_id",
    "node_type",
    "parent_node_id",
    "next_node_id",
    "source_id",
    "observed_date",
    "A01",
    "A02",
    "A03",
    "A04",
    "A05",
    "status",
    "notes",
)


def validate(rows: list[dict]) -> list[str]:
    errors: list[str] = []
    if not rows:
        return ["empty file"]
    missing = [c for c in REQUIRED if c not in rows[0]]
    if missing:
        return [f"missing columns: {missing}"]
    for i, row in enumerate(rows, start=2):
        rid = row.get("run_id", "")
        if not RUN_ID.match(rid):
            errors.append(f"L{i}: bad run_id {rid!r}")
        if row.get("node_type") not in ALLOWED_NODE_TYPE:
            errors.append(f"L{i}: bad node_type {row.get('node_type')!r}")
        if row.get("status") not in ALLOWED_STATUS:
            errors.append(f"L{i}: bad status {row.get('status')!r}")
        for c in CHECKS:
            v = str(row.get(c, "")).strip()
            if v not in ALLOWED_CHECK:
                errors.append(f"L{i}: bad {c}={v!r}")
        if not str(row.get("node_id", "")).strip():
            errors.append(f"L{i}: empty node_id")
        if not str(row.get("record_id", "")).strip():
            errors.append(f"L{i}: empty record_id")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description="MOKUREN CSV validator")
    p.add_argument("csv_path")
    args = p.parse_args()
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    errors = validate(rows)
    if errors:
        print("INVALID")
        for e in errors:
            print(e)
        return 1
    print("VALID")
    print(f"rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
