from typing import Literal

from pydantic import BaseModel, Field

from system.base.schema import GetMultiBaseModel


class TransferCreate(BaseModel):
    bank_profile_id: int
    type: Literal['PAYA']
    transfer_id: str | None
    batch_id: str | None
    merchant_id: int | None
    input_type: str
    input_unique_id: int
    amount: int
    description: str
    ext_service_name: Literal['jibit']


class TransferUpdate(BaseModel):
    amount: int | None
    description: str | None
    status: Literal['successful', 'failed'] | None
    error_message: str | None


class TransferGetMulti(GetMultiBaseModel):
    bank_profile_id: int | None
    batch_id: str | None
    transfer_id: str | None
    status: str | None

