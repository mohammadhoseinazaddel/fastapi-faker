import datetime
from enum import Enum

from pydantic import Field, BaseModel, validator

from system.config import settings


class TypeEnum(str, Enum):
    POST_PAY = 'POST_PAY'
    PAY_IN_FOUR = 'PAY_IN_FOUR'


class Title(BaseModel):
    title: str = \
        Field(...,
              title='Order title',
              description='Title of order',
              example="AIRPLANE",
              exclude=True
              )


class Type(BaseModel):
    type: TypeEnum = \
        Field(...,
              title='Order Type Id',
              description='Order Type Id',
              example="POST_PAY",
              )


class Commission(BaseModel):
    commission: str = \
        Field(...,
              title='Commission Type',
              description='commission type title',
              example="AIRPLANE",
              )


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


class UUID(BaseModel):
    uuid: str = \
        Field(...,
              title='Order identifier',
              description='Identifier of order',
              example="kdh6tr3sd6ijhgvd",
              )


class RedirectUrl(BaseModel):
    redirect_url: str = \
        Field(...,
              title='url to redirect from merchant',
              description="Merchant should redirect user to this url",
              example='https://wallpay-domain.com/redirect-url')


class CallBackUrl(BaseModel):
    callback_url: str = \
        Field(...,
              title='url to redirect from merchant',
              description="Merchant should redirect user to this url",
              example='https://wallpay-domain.com/redirect-url')

    # @TODO : Remove last slash from merchant redirect url
    # @validator('callback_url')
    # def remove_slash_from_end(cls, v):
    #     if v[::-1] == '/':
    #         v[::-1] = ''
    #         return v
    #     else:
    #         return v


class MerchantNameFa(BaseModel):
    merchant_name_fa: str = \
        Field(
            title='merchant-name',
            description='Name of merchant',
            example="علی بابا"
        )


class MerchantLogo(BaseModel):
    merchant_logo: str = \
        Field(
            title='merchant-logo',
            description='logo address of merchant',
            example="alibalba.ir/merchant/alibaba.svg"
        )


class Status(BaseModel):
    status: str = \
        Field(
            title='order-status',
            description='status of order',
            example="success"
        )


class Action(BaseModel):
    action: str = \
        Field(
            title='order-action',
            description='action of order',
            example="APPROVED"
        )


class UserCredit(BaseModel):
    user_credit: int = \
        Field(...,
              title='user-credit',
              description='Total credit of user',
              example=15000000,
              )

    @validator('user_credit')
    def convert_rial_to_tmn(cls, v):
        return int(v / 10)


class InUseCredit(BaseModel):
    in_use_credit: int = \
        Field(...,
              title='user-credit-in-use',
              description='Total credit of user',
              example=15000000,
              )

    @validator('in_use_credit')
    def convert_rial_to_tmn(cls, v):
        return int(v / 10)


class AmountToPay(BaseModel):
    amount_to_pay: int = \
        Field(...,
              title='amount-to-pay',
              description='The extra money that user should pay just right now',
              example=1500000)

    @validator('amount_to_pay')
    def convert_rial_to_tmn(cls, v):
        return int(v / 10)


class UseCollateral(BaseModel):
    use_collateral: bool = \
        Field(...,
              title='collateral-need',
              description='Does this order have collateral of not',
              example=15)


class ButtonActionName(BaseModel):
    action_btn_name: str = \
        Field(...,
              title='action-btn-name',
              description='persian name of btn',
              example='تکمیل فرآیند')


class CreatedDate(BaseModel):
    created_date: datetime.date = \
        Field(...,
              title='created_date',
              description='order create date',
              example='1400/01/01')


class RepayDate(BaseModel):
    repay_date: datetime.date = \
        Field(...,
              title='repay_date',
              description='order repay date',
              example='1400/02/05')


class PayCreateRequest(
    Title,
    Type,
    Commission,
    MerchantId,
    OrderId,
    UserId,
    InputAmount,
    CallBackUrl
):
    pass


class PayCreateResponse(
    UUID,
    CallBackUrl
):
    pass


class PayInfoResponse(
    UUID,
    MerchantNameFa,
    MerchantLogo,
    OutputAmount,
    Status,

):
    pass


class PayProcessResponse(
    Status,
    UUID,
    UserCredit,
    InUseCredit,
    AmountToPay,
    UseCollateral,
    OutputAmount,
    MerchantNameFa,
    MerchantLogo,
    Type,
):
    pass


class PayProcessRequest(
    UUID
):
    pass


class PayResultResponse(
    RedirectUrl
):
    pass


class PayActionResponse(
    UUID,
    OutputAmount,
    Status,
    Action,

):
    pass


class PayMyOrdersResponse(
    UUID,
    OutputAmount,
    InUseCredit,
    AmountToPay,
    CreatedDate,
    RepayDate,
    MerchantNameFa,
    MerchantLogo
):
    pass


class MerchantInfoOfOrderResponse(
    MerchantLogo,
    MerchantNameFa
):
    pass