from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from converter.validator import validate_csv

def test_invalid_check():
    errors = validate_csv(str(ROOT / "samples" / "sample_invalid.csv"))
    assert any("invalid_check" in e for e in errors)
