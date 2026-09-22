import pytest
from pydantic import ValidationError
from tests.schema import MGFCoreModel
BASE = {"run_id":"20260922-001","observed_date":"2026-02-28","status":"active","A01":"Y","A02":"N","A03":"0","A04":"Y","A05":"N","nodes":[],"edges":[]}

def test_extra_field_forbidden():
    p=dict(BASE); p["unknown"]="boom"
    with pytest.raises(ValidationError):
        MGFCoreModel.model_validate(p)

def test_strict_type_enforced():
    p=dict(BASE); p["run_id"]=123
    with pytest.raises(ValidationError):
        MGFCoreModel.model_validate(p)

def test_a_fields_domain_locked():
    p=dict(BASE); p["A01"]="YES"
    with pytest.raises(ValidationError):
        MGFCoreModel.model_validate(p)
