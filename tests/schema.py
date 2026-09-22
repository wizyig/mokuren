from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
YN0 = Literal["Y", "N", "0"]
class MGFCoreModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", validate_assignment=True)
    run_id: str = Field(min_length=1)
    observed_date: str = Field(pattern=r"^\\d{4}-\\d{2}-\\d{2}$")
    status: str = Field(min_length=1)
    A01: YN0
    A02: YN0
    A03: YN0
    A04: YN0
    A05: YN0
    nodes: list
    edges: list
