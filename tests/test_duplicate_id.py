from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from converter.validator import validate_csv

def test_duplicate_id():
    errors = validate_csv(str(ROOT / "samples" / "duplicate.csv"))
    assert any("duplicate" in e for e in errors)
