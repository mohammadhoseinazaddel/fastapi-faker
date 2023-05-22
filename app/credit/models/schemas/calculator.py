from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class CalculatorCreateSchema(BaseModel):
    credit_id: int
    non_free_credit: int
    used_non_free_credit: int
    free_credit: int
    used_free_credit: int
    asset_json: dict
    cs: float
    input_type: str | None
    input_unique_id: int | None


class CalculatorUpdateSchema(BaseModel):
    pass


class CalculatorGetMulti(GetMultiBaseModel):
    credit_id: int | None
    input_type: str | None
    input_unique_id: int | None
