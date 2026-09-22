from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from converter.validator import validate_csv

def test_invalid_date():
    errors = validate_csv(str(ROOT / "samples" / "invalid_date.csv"))
    assert any("invalid_date" in e for e in errors)
