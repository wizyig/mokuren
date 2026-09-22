from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from converter.validator import validate_csv

def test_valid_csv():
    assert validate_csv(str(ROOT / "samples" / "sample_valid.csv")) == []
