import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from system.base.schema import GetMultiBaseModel


def _generate_identifier():
    return str(uuid.uuid4()).replace('-', '')[0:16]


class TypeEnum(str, Enum):
    POST_PAY = 'POST_PAY'
    PAY_IN_FOUR = 'PAY_IN_FOUR'


class StatusEnum(str, Enum):
    WAIT_PROCESS = 'WAIT_PROCESS'
    WAIT_WALLEX = 'WAIT_WALLEX'
    WAIT_PAYMENT = 'WAIT_PAYMENT'
    WAIT_COLLATERAL = 'WAIT_COLLATERAL'
    PROCESS = 'PROCESS'
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'
    FAIL_FILL = 'FAIL_FILL'
    FAIL_WALLEX = 'FAIL_WALLEX'
    FAIL_PAYMENT = 'FAIL_PAYMENT'
    REFUNDING = 'REFUNDING'
    REFUNDED = 'REFUNDED'
    WAIT_IBAN_TO_REFUND = 'WAIT_IBAN_TO_REFUND'


class ActionEnum(str, Enum):
    UNVERIFIED = 'UNVERIFIED'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


class CreatePayOrderSchema(BaseModel):
    title: str
    merchant_order_id: str
    merchant_id: int
    merchant_user_id: str
    type: TypeEnum
    amount: int
    identifier: uuid.UUID = Field(default_factory=_generate_identifier)
    merchant_redirect_url: str
    status: StatusEnum = StatusEnum.WAIT_PROCESS
    action: ActionEnum = ActionEnum.UNVERIFIED
    commission_id: int


class UpdatePayOrder(BaseModel):
    title: str | None
    id: int | None
    type_id: int | None
    merchant_id: int | None
    merchant_user_id: str | None
    amount: float | None
    user_id: int | None
    status: StatusEnum | None
    action: StatusEnum | None
    settle_id: int | None
    merchant_pay_req_id: int | None
    deleted_at: datetime | None
    paid_at: datetime | None


class GetMultiOrdPay(GetMultiBaseModel):
    identifier: str | None
    user_id: int | None
    amount: int | None
    merchant_id: int | None
    status: str | None
    action: str | None
    merchant_order_id: str | None
    created_at: datetime | None
    paid_at__isnull: bool | None
    created_at__lt: datetime | None
    commission_id: int | None
    settle_id: int | None
