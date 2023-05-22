from uuid import UUID

from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field, validator


# Base Classes
class ModelId(BaseModel):
    id: int = \
        Field(...,
              title='settlement id',
              description='db id of settlement record',
              example=13
              )


class TransferId(BaseModel):
    transfer_id: int | None = \
        Field(...,
              title='settlement transfer id',
              description='db transfer id of settlement record',
              example=13
              )


class OrderUuid(BaseModel):
    order_uuid: str | None = \
        Field(...,
              title='settlement order  uuid',
              description='db order uuid of settlement record',
              example=13
              )


class OrderId(BaseModel):
    order_id: int = \
        Field(...,
              title='settlement order  id',
              description='db order id of settlement record',
              example=13
              )


class Amount(BaseModel):
    amount: int = \
        Field(...,
              title='settlement amount',
              description='price of settlement in tmn',
              example=250000
              )

    @validator('amount')
    def convert_rial_to_tmn(cls, v):
        return v / 10


class OrderAmount(BaseModel):
    order_amount: int = \
        Field(...,
              title='order amount',
              description='price of order in tmn',
              example=250000
              )

    @validator('order_amount')
    def convert_rial_to_tmn(cls, v):
        return v / 10


class CreatedDate(BaseModel):
    created_at: datetime | None = \
        Field(...,
              title='create time of settlement',
              description='',
              example='2023-01-08T18:18:28.484594'
              )


class MerchantId(BaseModel):
    merchant_id: int = \
        Field(...,
              title='merchant id',
              description='id of merchant',
              example=2
              )


class MerchantOrderId(BaseModel):
    merchant_order_id: str | None = \
        Field(...,
              title='merchant order id',
              description='order id of merchant',
              example=2
              )


class SettlementType(BaseModel):
    type: str = \
        Field(...,
              title='type of settlement',
              description='type of settlement',
              example=""
              )


# Merged Classes

class TransferDetailResponse(
    ModelId,
    CreatedDate,
    SettlementType,
    OrderId,
    OrderUuid,
    OrderAmount,
    Amount,
    TransferId,
    MerchantId,
    MerchantOrderId,
):
    pass


class OrderCreationPeriod(BaseModel):
    start_time: datetime = Field(...,
                                 title='From',
                                 description='Start time for the query.'
                                 )
    end_time: datetime = Field(...,
                               title='Until',
                               description='End time for the query.'
                               )


class PaymentSummary(BaseModel):
    daily: int = Field(...,
                       title='Daily Payment Summary',
                       description='Daily Payment Summary.'
                       )
    monthly: int = Field(...,
                         title='Monthly Payment Summary',
                         description='Monthly Payment Summary.'
                         )


class SettlementSummary(BaseModel):
    credit: int = Field(...,
                        title='Credit Settlement',
                        description='Credit settlement.'
                        )
    pgw: int = Field(...,
                     title='Payment Gateway Settlement',
                     description='Payment gateway settlement.'
                     )


class PaymentPlotRow(BaseModel):
    time: datetime
    credit: int
    pgw: int


class MerchantDashboardRequest(BaseModel):
    start_time: Optional[datetime] = datetime.now() - timedelta(days=30)
    end_time: Optional[datetime] = datetime.now()


class MerchantDashboardSummaryResponse(BaseModel):
    credit: PaymentSummary
    pgw: PaymentSummary
    unsettled: SettlementSummary


class MerchantDashboardPlotResponse(BaseModel):
    plot: List[PaymentPlotRow]
