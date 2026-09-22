from pathlib import Path
import sys
import pytest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from converter.coverage import GOLDEN_CASES
from converter.io import core_snapshot, dump_csv, dump_yaml, load_csv, load_yaml
CASES = list(GOLDEN_CASES)

@pytest.mark.parametrize("case", CASES)
def test_golden_core_csv_yaml(case):
    stem = GOLDEN_CASES[case]["stem"]
    assert core_snapshot(load_csv(ROOT / "samples" / f"{stem}.csv")) == core_snapshot(load_yaml(ROOT / "samples" / f"{stem}.yaml"))

@pytest.mark.parametrize("case", CASES)
def test_golden_csv_yaml_csv(case, tmp_path):
    stem = GOLDEN_CASES[case]["stem"]
    data = load_csv(ROOT / "samples" / f"{stem}.csv")
    dump_yaml(data, tmp_path / "out.yaml")
    dump_csv(load_yaml(tmp_path / "out.yaml"), tmp_path / "roundtrip.csv")
    assert core_snapshot(data) == core_snapshot(load_csv(tmp_path / "roundtrip.csv"))

@pytest.mark.parametrize("case", CASES)
def test_golden_yaml_csv_yaml(case, tmp_path):
    stem = GOLDEN_CASES[case]["stem"]
    data = load_yaml(ROOT / "samples" / f"{stem}.yaml")
    dump_csv(data, tmp_path / "out.csv")
    dump_yaml(load_csv(tmp_path / "out.csv"), tmp_path / "roundtrip.yaml")
    assert core_snapshot(data) == core_snapshot(load_yaml(tmp_path / "roundtrip.yaml"))
