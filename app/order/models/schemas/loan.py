from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class LoanCreateSchema(BaseModel):
    fund_id: int
    loan_position: int
    amount: float
    settlement_time: datetime
    user_id: int
    payment_detail_id: None | int
    paid_at: datetime | None


class LoanUpdateSchema(BaseModel):
    payment_id: None | int
    paid_at: datetime | None
    payment_detail_id: int | None


class LoanGetMultiSchema(GetMultiBaseModel):
    fund_id: int | None
    loan_position: int | None
    payment_id: int | None
    user_id: int | None
    payment_detail_id: int | None
    paid_at: datetime | None
    paid_at__isnull: bool | None
    deleted_at__isnull: bool | None


class GetMultiFunLoan(GetMultiBaseModel):
    pass