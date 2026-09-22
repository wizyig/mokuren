#!/usr/bin/env python3
"""mokuren CLI. argparse only."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from converter.csv_to_yaml import csv_to_mgf, dump_yaml
from converter.validator import validate_csv, validate_yaml
from converter.yaml_to_graph import to_dot
from converter.csv_to_yaml import csv_to_mgf as load_csv_mgf

def cmd_validate(args):
    path = args.file
    errors = validate_yaml(path) if path.endswith((".yaml", ".yml")) else validate_csv(path)
    if errors:
        print("VALIDATION_FAILED")
        for e in errors:
            print(f"- {e}")
        return 1
    print("VALIDATION_PASSED")
    return 0

def cmd_csv_to_yaml(args):
    text = dump_yaml(csv_to_mgf(args.file, args.dataset_type, args.sample_data))
    Path(args.output).write_text(text, encoding="utf-8") if args.output else sys.stdout.write(text)
    return 0

def cmd_graph(args):
    path = args.file
    if path.endswith((".yaml", ".yml")):
        from converter.yaml_to_graph import _load
        data = _load(path)
    else:
        data = load_csv_mgf(path)
    text = to_dot(data)
    Path(args.output).write_text(text, encoding="utf-8") if args.output else sys.stdout.write(text)
    return 0

def main():
    parser = argparse.ArgumentParser(prog="mokuren")
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate")
    v.add_argument("file")
    v.set_defaults(func=cmd_validate)
    c = sub.add_parser("to-yaml")
    c.add_argument("file")
    c.add_argument("-o", "--output")
    c.add_argument("--dataset-type", default="observed")
    c.add_argument("--sample-data", action="store_true")
    c.set_defaults(func=cmd_csv_to_yaml)
    g = sub.add_parser("graph")
    g.add_argument("file")
    g.add_argument("-o", "--output")
    g.set_defaults(func=cmd_graph)
    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
