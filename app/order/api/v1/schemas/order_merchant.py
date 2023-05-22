from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import Optional


class OrderWallpayID(BaseModel):
    id: str = Field(...,
        title='Order Wallpay ID',
        description='Order Wallpay ID.',
        example='1234567890123456'
    )


class OrderCreationPeriod(BaseModel):
    start_time: datetime = Field(...,
        title='From',
        description='Start time for the query.'
    )
    end_time: datetime = Field(...,
        title='Until',
        description='End time for the query.'
    )


class OrderTypes(str, Enum):
    post_pay = 'POST_PAY'
    pay_in_four = 'PAY_IN_FOUR'

class OrderType(BaseModel):
    type: OrderTypes = Field(...,
        title='Order Type',
        description='Type of the Order.'
    )


class OrderCommission(BaseModel):
    id: int
    category: Optional[str]
    pgw_commission_constant: Optional[int]
    pgw_commission_rate: float
    pgw_fee_constant: int
    pgw_fee_rate: float
    credit_commission_constant: int
    credit_commission_rate: float
    credit_limit: int
    decrease_fee_on_pay_gw_settle: bool
    decrease_commission_on_refund: bool


class OrderStatusTypes(str, Enum):
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'
    FAIL_FILL = 'FAIL_FILL'
    FAIL_WALLEX = 'FAIL_WALLEX'
    FAIL_PAYMENT = 'FAIL_PAYMENT'
    WAIT_PROCESS = 'WAIT_PROCESS'
    WAIT_WALLEX = 'WAIT_WALLEX'
    WAIT_PAYMENT = 'WAIT_PAYMENT'
    WAIT_COLLATERAL = 'WAIT_COLLATERAL'
    PROCESS = 'PROCESS'
    REFUNDED = 'REFUNDED'
    WAIT_IBAN_TO_REFUND = 'WAIT_IBAN_TO_REFUND'
    REFUNDING = 'REFUNDING'
    

class OrderStatus(BaseModel):
    status: OrderStatusTypes = Field(...,
        title='Order Status',
        description='Order Status.'
    )


class OrderAmount(BaseModel):
    amount: int = Field(...,
        title='Order Amount',
        description='Order Price in Iranian Toman.',
        example=250000
    )

    @validator('amount')
    def convert_rial_to_tmn(cls, v):
        return v / 10


class OrderTime(BaseModel):
    created_at: datetime = Field(...,
        title='Order Time',
        description='Order Creation Time'
    )


class OrderStoreID(BaseModel):
    title: str = Field(...,
        title='Order Store ID',
        description='Order Store ID.',
        example='1234567890123456'
    )


class OrdersMerchantRequest(BaseModel):
    start_time: Optional[datetime] = datetime.now() - timedelta(days=30)
    end_time: Optional[datetime] = datetime.now()
    order_id: Optional[int]
    type: Optional[OrderTypes]
    commission_id: Optional[int]
    status: Optional[OrderStatusTypes]
    page_size: Optional[int] = 10
    page_number: Optional[int] = 1


class OrdersMerchantBaseResponse(
    OrderStatus,
    OrderType,
    OrderAmount,
    OrderTime,
    OrderStoreID,
    OrderWallpayID
):
    pass

class OrdersMerchantResponse(
    OrdersMerchantBaseResponse
):
    commission: str


class OrderMerchantResponse(
    OrdersMerchantResponse
):
    commission: Optional[OrderCommission]
    credit: Optional[int]
    pgw: Optional[int]


class OrderGetSchema(BaseModel):
    order_id: int | None
    user_id: int | None
    created_at_gte: datetime | None
    created_at_lte: datetime | None
    type: OrderTypes | None
    commission_id: int | None
    status: OrderStatusTypes | None
    merchant_id: int | None
