import re
from pathlib import Path
from tests.spec_registry import EXCLUDED_CONDITIONS, SPEC_FIXTURES, SPEC_IDS

def test_validation_scope_contains_all_ids():
    doc = Path("docs/validation_scope.md").read_text(encoding="utf-8")
    found = set(re.findall(r"(CORE-\\d+|COND-\\d+)", doc))
    assert SPEC_IDS <= found

def test_exclusion_ids_match_spec():
    assert set(EXCLUDED_CONDITIONS) == {"COND-101","COND-102","COND-103","COND-104","COND-105"}

def test_all_fixture_files_exist():
    root = Path("tests/fixtures/v1_1")
    missing = [f"{k}:{v}" for k,v in SPEC_FIXTURES.items() if not (root/v).exists()]
    assert not missing
