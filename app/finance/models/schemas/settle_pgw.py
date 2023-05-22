from typing import Literal
from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class SettlePgwCreate(BaseModel):
    order_id: int
    order_uuid: str
    type: Literal['pay', 'reverse', 'refund']
    merchant_id: int
    amount: int


class SettlePgwUpdate(BaseModel):
    transfer_id: int | None


class SettlePgwGetMulti(GetMultiBaseModel):
    order_id: int | None
    type: Literal['pay', 'reverse', 'refund'] | None
    merchant_id: int | None
    amount: int | None
    transfer_id: int | None
    order_uuid: str | None
    transfer_id__isnull: bool | None
