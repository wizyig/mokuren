from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from converter.io import core_snapshot, dump_csv, dump_yaml, load_csv, load_yaml

def test_golden_core_csv_yaml():
    assert core_snapshot(load_csv(ROOT / "samples" / "golden.csv")) == core_snapshot(load_yaml(ROOT / "samples" / "golden.yaml"))

def test_golden_csv_yaml_csv(tmp_path):
    data = load_csv(ROOT / "samples" / "golden.csv")
    dump_yaml(data, tmp_path / "out.yaml")
    restored = load_yaml(tmp_path / "out.yaml")
    dump_csv(restored, tmp_path / "roundtrip.csv")
    assert core_snapshot(data) == core_snapshot(load_csv(tmp_path / "roundtrip.csv"))
    assert (tmp_path / "roundtrip.csv").read_text(encoding="utf-8") == dump_csv(data)

def test_golden_yaml_csv_yaml(tmp_path):
    data = load_yaml(ROOT / "samples" / "golden.yaml")
    dump_csv(data, tmp_path / "out.csv")
    restored = load_csv(tmp_path / "out.csv")
    dump_yaml(restored, tmp_path / "roundtrip.yaml")
    assert core_snapshot(data) == core_snapshot(load_yaml(tmp_path / "roundtrip.yaml"))
