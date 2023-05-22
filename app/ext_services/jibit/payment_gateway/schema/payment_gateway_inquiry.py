from typing import Literal, Any
from pydantic import BaseModel, Field


class PaymentGatewayInquiry(BaseModel):
    purchase_id: str
    amount: int | None
    wage: int | None
    fee: int | None
    fee_payment_type: str | None
    currency: str | None
    callback_url: str | None
    psp_status: str | None
    client_ref_num: str | None
    psp_name: str | None
    psp_rrn: str | None
    psp_ref_num: str | None
    psp_trace_num: str | None
    expire_date: str | None
    user_identifier: str | None
    payer_mobile_num: str | None
    addition_date: dict | None
    psp_masked_card_num: str | None
    payer_ip: str | None
    redirect_payer_ip: str | None
    psp_settled: str | None
    created_at: str | None
    billing_date: str | None
    verified_at: str | None
    psp_settled_at: str | None
