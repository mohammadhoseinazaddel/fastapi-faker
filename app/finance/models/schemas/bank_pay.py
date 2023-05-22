from typing import Optional, Literal
from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class CreateBankPayment(BaseModel):
    bank_payment_id: int | None
    input_type: Literal['pay_order']
    input_unique_id: int
    user_id: int
    amount: int
    wage: Optional[int]
    description: Optional[str]
    type: str | None


class UpdateBankPayment(BaseModel):
    user_id: Optional[int]
    amount: Optional[int]
    description: Optional[str]

    status: Optional[str]
    success_pgw_id: int | None


class GetMultiFinBankPayment(GetMultiBaseModel):
    input_type: str | None
    input_unique_id: int | None
    user_id: int | None
    amount: int | None
    wage: int | None
    description: str | None
    type: str | None
    bank_payment_id: int | None
    success_pgw_id: int | None

