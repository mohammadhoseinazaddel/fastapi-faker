import datetime

from pydantic import BaseModel, Field, validator


class OrderId(BaseModel):
    id: int = \
        Field(...,
              title='pay order id',
              description='db id of order record',
              example=13
              )


class Status(BaseModel):
    status: str = \
        Field(...,
              title='order-status',
              description='Id of order',
              example='set-by-merchant'
              )


class Title(BaseModel):
    title: str = \
        Field(...,
              title='title',
              description='title of order',
              example='یخچال'
              )


class Uuid(BaseModel):
    uuid: str = \
        Field(...,
              title='order-uuid',
              description='identifier of order',
              example='1'
              )


class UserId(BaseModel):
    user_id: int | None = \
        Field(...,
              title='order user id',
              description='user id of order',
              example=89
              )


class Type(BaseModel):
    type: str | None = \
        Field(...,
              title='order type',
              description='type of order',
              example='PostPay'
              )


class Amount(BaseModel):
    amount: int = \
        Field(...,
              title='order amount',
              description='price of order in tmn',
              example=250000
              )

    @validator('amount')
    def convert_rial_to_tmn(cls, v):
        return v / 10


class UserPhoneNumber(BaseModel):
    user_phone_number: str = \
        Field(...,
              title='user phone number',
              description='price of order ',
              example=250000
              )


class MerchantUserId(BaseModel):
    merchant_user_id: str = \
        Field(...,
              title='merchant user id',
              description='User id in merchant side',
              example='dkdjs84'
              )


class PaidAmount(BaseModel):
    paid_amount: int = \
        Field(...,
              title='paid amount',
              description='amount that already paid in tmn',
              example=250000
              )

    @validator('paid_amount')
    def convert_rial_to_tmn(cls, v):
        return v / 10


class RemianAmount(BaseModel):
    remain_amount: int = \
        Field(...,
              title='remain amount',
              description='remain amount',
              example=500000
              )

    @validator('remain_amount')
    def convert_rial_to_tmn(cls, v):
        return v / 10


class Commission(BaseModel):
    commission: int = \
        Field(...,
              title='commission',
              description='commission',
              example=10000
              )

    @validator('commission')
    def convert_rial_to_tmn(cls, v):
        return v / 10


class CreditUsedAmount(BaseModel):
    credit_used_amount: int = \
        Field(...,
              title='credit used amount',
              description='credit_used_amount',
              example=10000
              )

    @validator('credit_used_amount')
    def convert_rial_to_tmn(cls, v):
        return v / 10


class Gateway(BaseModel):
    gateway: int = \
        Field(...,
              title='gateway',
              description='used free credit + used non free credit',
              example=10000
              )

    @validator('gateway')
    def convert_rial_to_tmn(cls, v):
        return v / 10


class CreatedDate(BaseModel):
    created_at: datetime.datetime = \
        Field(...,
              title='create time of order',
              description='',
              example='2023-01-08T18:18:28.484594'
              )


class FirstPayId(BaseModel):
    first_payment_id: int | None = \
        Field(...,
              title='first payment id',
              description='first payment id',
              example=1
              )


class PayOrderDetailResponse(
    OrderId,
    Status,
    Type,
    Title,
    Uuid,
    UserId,
    UserPhoneNumber,
    MerchantUserId,
    Amount,
    PaidAmount,
    RemianAmount,
    Commission,
    FirstPayId,
    CreatedDate
):
    pass


class UserOrdersResponse(
    OrderId,
    UserPhoneNumber,
    CreatedDate,
    MerchantUserId,
    Amount,
    Commission,
    CreditUsedAmount,
    Gateway
):
    pass


class CqGetOrderDetails(BaseModel):
    phone_number: str | None
    created_at_ge: datetime.datetime | None
    created_at_le: datetime.datetime | None
    order_price_ge: float | None
    order_price_le: float | None
    order_status: str | None


class CqGetUserOrders(BaseModel):
    user_id: int | None
    created_at_ge: datetime.datetime | None
    created_at_le: datetime.datetime | None
    order_price_ge: float | None
    order_price_le: float | None
