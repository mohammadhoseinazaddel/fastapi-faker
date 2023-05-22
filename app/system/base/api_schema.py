from pydantic import Field, BaseModel, validator

from system.config import settings


class InputAmount(BaseModel):
    amount: int = \
        Field(...,
              ge=settings.MINIMUM_PAY_ORDER_AMOUNT,
              le=settings.MAXIMUM_PAY_ORDER_AMOUNT,
              title='Order Amount',
              description='Order Amount',
              example=250000,
              )

    @validator('amount')
    def change_tmn_to_rial(cls, v):
        return v * 10


class OutputAmount(BaseModel):
    amount: int = \
        Field(...,
              ge=settings.MINIMUM_PAY_ORDER_AMOUNT,
              le=settings.MAXIMUM_PAY_ORDER_AMOUNT,
              title='Order Amount',
              description='Order Amount',
              example=250000,
              )

    @validator('amount')
    def change_rial_to_tmn(cls, v):
        return v / 10


class MerchantId(BaseModel):
    merchant_id: int = \
        Field(...,
              title='Merchant Id',
              description='Merchant Id',
              example=1,
              )


class OrderId(BaseModel):
    order_id: str = \
        Field(...,
              title='Order Id on Merchant side',
              description='Order Id on Merchant side',
              example='1232-1242-124124-1223',
              )


class UserId(BaseModel):
    user_id: str = \
        Field(...,
              min_length=1,
              max_length=35,
              title='User Id on Merchant side',
              description='User Id on Merchant side',
              example='100054',
              )


class OrderUUID(BaseModel):
    order_uuid: str = \
        Field(...,
              title='Order identifier',
              description='Identifier of order',
              example="kdh6tr3sd6ijhgvd",
              )


class OrderStatus(BaseModel):
    order_status: str = \
        Field(...,
              title='order ststus',
              description='order status is success',
              example="Success",
              )


class MerchantLogoAddress(BaseModel):
    merchant_logo_address: str = \
        Field(...,
              title='to-pay-amount',
              description='amount to pay, if is not 0 it meant user can pay',
              example=500000,
              )


class MerchantNameFa(BaseModel):
    merchant_name_fa: str = \
        Field(...,
              title='persian name of merchant',
              description='persian name of merchant',
              example='علی بابا',
              )


class OrderTotalAmountOutput(BaseModel):
    order_total_amount: int = \
        Field(...,
              title='total pay amount in tmn',
              description='total pay amount in tmn',
              example='',
              )

    @validator('order_total_amount')
    def change_rial_to_tmn(cls, v):
        return v / 10
