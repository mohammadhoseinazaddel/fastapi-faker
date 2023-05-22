from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator


################################## Base Classes ##################################
class ModelId(BaseModel):
    id: int = \
        Field(...,
              title='transfer id',
              description='db id of transfer record',
              example=13
              )


class BankTransferUuid(BaseModel):
    bank_transfer_id: str | None = \
        Field(...,
              title='transfer UUID',
              description='db transfer UUID record',
              example="d48edaa6-871a-4082-a196-4daab372d4a1"
              )


class Amount(BaseModel):
    amount: int | None = \
        Field(...,
              title='transfer amount',
              description='price of transfer in tmn',
              example=250000
              )

    @validator('amount')
    def convert_rial_to_tmn(cls, v):
        return v / 10


class Reason(BaseModel):
    reason: str = \
        Field(...,
              title='reason',
              description='reason of payment(pay - repay)',
              example='pay'
              )


class CreatedDate(BaseModel):
    created_at: datetime | None = \
        Field(...,
              title='create time of transfer',
              description='',
              example='2023-01-08T18:18:28.484594'
              )


class Status(BaseModel):
    status: str | None = \
        Field(...,
              title='payment status',
              description='payment status',
              example='FAILED'
              )


class GatewayName(BaseModel):
    gateway_name: str = \
        Field(...,
              title='gateway name',
              description='gateway name',
              example='jibit'
              )


class UserPhoneNumber(BaseModel):
    user_phone_number: str = \
        Field(...,
              title='user phone number',
              description='user phone number',
              example='0912345678'
              )


class UserId(BaseModel):
    user_id: int = \
        Field(...,
              title='user id',
              description='id of user',
              example=2
              )


class Iban(BaseModel):
    iban: str | None = \
        Field(...,
              title='iban number',
              description='iban number of user',
              example="IR710570029971601460641001"
              )


class BankAccountNumber(BaseModel):
    account_no: str | None = \
        Field(...,
              title='bank account number',
              description='bank account number',
              example="60641001"
              )


class BankName(BaseModel):
    bank_name: str | None = \
        Field(...,
              title='bank name',
              description='bank name',
              example="karafarin"
              )


class TransferType(BaseModel):
    type: str | None = \
        Field(...,
              title='type of transfer Credit/Gateway',
              description='type of transfer Credit/Gateway',
              example=""
              )


class BankPaymentDetailResponse(
    ModelId,
    Amount,
    Reason,
    CreatedDate,
    Status,
    GatewayName,
    UserPhoneNumber,
    UserId,
):
    pass


class TransfersAdminResponse(
    ModelId,
    BankTransferUuid,
    CreatedDate,
    Iban,
    BankAccountNumber,
    BankName,
    Amount,
    TransferType

):
    pass


class CqGetTransferList(BaseModel):
    created_at_ge: datetime | None
    created_at_le: datetime | None
    transfer_price_ge: float | None
    transfer_price_le: float | None
    merchant_id: int | None
    bank_name: str | None
    transfer_type: str | None
    transfer_id: int | None


class CqGetSettleDetail(BaseModel):
    created_at_ge: datetime | None
    created_at_le: datetime | None
    transfer_price_ge: float | None
    transfer_price_le: float | None
    transfer_id: int | None
    merchant_id: int | None
    settlement_id: int | None
    unsettled: bool | None
