from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from converter.validator import validate_csv, validate_date

def test_feb_31_rejected():
    assert validate_date("2026-02-31") is False
    errors = validate_csv(str(ROOT / "samples" / "invalid_calendar.csv"))
    assert any("invalid_date=2026-02-31" in e for e in errors)
    assert any("invalid_date=2026-13-01" in e for e in errors)

def test_real_day_accepted():
    assert validate_date("2026-02-28") is True
