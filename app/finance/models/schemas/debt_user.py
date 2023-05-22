from typing import Literal

from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class DebtUserCreate(BaseModel):
    user_id: int
    amount: int
    input_type: Literal['OrdPay', 'repay', 'refund']
    input_unique_id: int
    order_id: int


class DebtUserUpdate(BaseModel):
    pass


class DebtUserGetMulti(GetMultiBaseModel):
    user_id: int | None
    input_type: str | None
    input_unique_id: int | None
    order_id: int | None


