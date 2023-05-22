from pydantic import Field, validator

from system.base.api_schema import InputAmount, OrderUUID, OrderStatus, MerchantLogoAddress, MerchantNameFa, \
    OrderTotalAmountOutput


class RefundRequest(OrderUUID, InputAmount):
    pass


class RefundResponse(OrderUUID, OrderStatus):
    pass


class RefundDetailRequest(OrderUUID):
    pass


class RefundDetailResponse(
    MerchantLogoAddress,
    MerchantNameFa,
    OrderTotalAmountOutput,
):
    credit_amount_to_refund: int = \
        Field(...,
              title='total credit amount to refund',
              description='total credit amount to refund in tmn',
              example=50000,
              )

    tmn_amount_to_refund: int = \
        Field(...,
              title='total tmn amount to refund',
              description='total tmn amount to refund',
              example=200000,
              )

    @validator('credit_amount_to_refund', 'tmn_amount_to_refund')
    def convert_rial_to_tmn(cls, v):
        return v / 10


class SubmitRefundAfterAddBankProfileRequest(
    OrderUUID
):
    pass


class SubmitRefundAfterAddBankProfileResponse(OrderUUID, OrderStatus):
    pass