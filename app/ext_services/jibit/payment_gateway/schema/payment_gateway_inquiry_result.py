from typing import List
from pydantic import BaseModel
from ext_services.jibit.payment_gateway.schema.payment_gateway_inquiry import PaymentGatewayInquiry


class PaymentGatewayInquiryResult(BaseModel):
    page_number: int | None
    size: int | None
    number_of_elements: int | None
    has_next: bool | None
    has_previous: bool | None
    purchases: List[PaymentGatewayInquiry] | None

