import uuid as uuid
from typing import Literal

from pydantic import BaseModel, Field

from system.base.schema import GetMultiBaseModel


def _generate_identifier():
    return str(uuid.uuid4()).replace('-', '')[0:16]


class RefundCreate(BaseModel):
    uuid: str = Field(default_factory=_generate_identifier)
    order_id: int
    order_uuid: str
    merchant_id: int
    merchant_user_id: int
    amount: int
    order_user_id: int
    status: Literal['REQUESTED_FROM_MERCHANT', 'DONE']


class RefundUpdate(BaseModel):
    status: Literal['REQUESTED_FROM_MERCHANT', 'DONE'] | None
    refund_by_debt: int | None
    refund_by_rial: int | None


class RefundGetMulti(GetMultiBaseModel):
    order_uuid: str | None
    order_id: int | None


