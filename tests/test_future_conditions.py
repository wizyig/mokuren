import pytest
from tests.spec_registry import EXCLUDED_CONDITIONS
@pytest.mark.parametrize("cond_id", list(EXCLUDED_CONDITIONS))
def test_v1_1_conditions_reserved(cond_id):
    assert cond_id.startswith("COND-")
