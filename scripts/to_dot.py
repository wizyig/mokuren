#!/usr/bin/env python3
"""CSV -> Graphviz DOT. No scoring. Attributes stay as observed."""

from __future__ import annotations

import argparse
import csv
import sys


def row_pattern(row: dict) -> str:
    return " ".join(str(row.get(k, "0")) for k in ("A01", "A02", "A03", "A04", "A05"))


def emit_dot(rows: list[dict]) -> str:
    lines = ["digraph MOKUREN {", "  rankdir=TB;", "  node [shape=box, fontname=monospace];"]
    seen = set()
    for row in rows:
        node = (row.get("node_id") or "").strip()
        if not node or node in seen:
            continue
        seen.add(node)
        ntype = row.get("node_type") or ""
        status = row.get("status") or ""
        pat = row_pattern(row)
        label = f"{node}\\n{ntype}\\n[{pat}]\\n{status}"
        lines.append(f'  "{node}" [label="{label}"];')
    for row in rows:
        node = (row.get("node_id") or "").strip()
        nxt = (row.get("next_node_id") or "").strip()
        if node and nxt:
            lines.append(f'  "{node}" -> "{nxt}";')
    lines.append("}")
    return "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description="MOKUREN CSV to DOT")
    p.add_argument("csv_path")
    p.add_argument("-o", "--output")
    args = p.parse_args()
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = emit_dot(rows)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
