from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from converter.coverage import CORE_FIELDS, GOLDEN_CASES, V1_0_EXCLUDED_VALIDATIONS
from converter.validator import validate_csv

def test_v1_0_coverage_locked():
    assert CORE_FIELDS == ("run_id", "nodes", "edges", "observed_date", "status", "A01", "A02", "A03", "A04", "A05")
    assert set(V1_0_EXCLUDED_VALIDATIONS) == {"COND-101", "COND-102", "COND-103", "COND-104", "COND-105"}

def test_v1_0_does_not_claim_cond():
    for case in GOLDEN_CASES.values():
        assert case["validates_cond"] == frozenset()

def test_extensions_roundtrip_allowed_without_cond():
    assert validate_csv(str(ROOT / "samples" / "golden_extensions.csv")) == []
    assert GOLDEN_CASES["extensions"]["pending_cond"] == frozenset({"COND-102", "COND-103", "COND-105"})
