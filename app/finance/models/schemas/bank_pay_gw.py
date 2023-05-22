from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class CreatePaymentGateway(BaseModel):
    type: Literal['pay', 'reverse', 'refund']
    payment_gateway_id: int | None
    bank_payment_id: int
    amount: int
    gateway_name: Optional[str]
    description: Optional[str]
    reversed_at: datetime | None
    reverse_status: str | None


class UpdatePaymentGateway(BaseModel):
    description: Optional[str]

    status: Optional[str]

    psp_purchase_id: Optional[str]
    psp_switching_url: Optional[str]
    psp_status: Optional[str]  # IN_PROGRESS, READY_TO_VERIFY,EXPIRED, FAILED, REVERSED, SUCCESS, and UNKNOWN.
    psp_trace_no: Optional[str]
    payer_ip: Optional[str]
    callback_status: Optional[str]
    psp_ref_num: Optional[str]
    payer_masked_card_num: Optional[str]
    psp_rrn: Optional[str]
    psp_name: Optional[str]

    reversed_at: datetime | None
    reverse_status: str | None

    refund_batch_id: str | None
    refund_transfer_id: str | None


class GetMultiFinPaymentGateway(GetMultiBaseModel):
    type: Literal['pay', 'reverse', 'refund'] | None
    payment_gateway_id: int | None
    status: Optional[str]
    psp_purchase_id: Optional[int]
    psp_switching_url: Optional[str]
    psp_status: Optional[str]  # IN_PROGRESS, READY_TO_VERIFY,EXPIRED, FAILED, REVERSED, SUCCESS, and UNKNOWN.
    psp_trace_no: Optional[str]
    payer_ip: Optional[str]
    callback_status: Optional[str]
    psp_ref_num: Optional[str]
    payer_masked_card_num: Optional[str]
    psp_rrn: Optional[str]
    psp_name: Optional[str]
    bank_payment_id: Optional[int]
    amount__gt: Optional[int]
    status__isnull: bool | None
    gateway_name: Optional[str]
    description: Optional[str]
    ref_num: Optional[str]

    reverse_status: str | None

    refund_batch_id: str | None
    refund_transfer_id: str | None


class CqGetAllPaymentGateways(BaseModel):
    phone_number: str | None
    created_at_ge: datetime | None
    created_at_le: datetime | None
    price_ge: float | None
    price_le: float | None

