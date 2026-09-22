import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def test_schema_load():
    schema = json.loads((ROOT / "schema" / "mgf.schema.json").read_text(encoding="utf-8"))
    assert schema["title"] == "MGF v1"

def test_no_extra_props():
    schema = json.loads((ROOT / "schema" / "mgf.schema.json").read_text(encoding="utf-8"))
    assert schema["additionalProperties"] is False
