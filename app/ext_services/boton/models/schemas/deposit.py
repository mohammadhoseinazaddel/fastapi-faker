from enum import Enum

from pydantic import BaseModel
from system.base.schema import GetMultiBaseModel


class SystemStatusEnum(str, Enum):
    REGISTERED = 'REGISTERED'
    UPDATED = 'UPDATED'
    INCREASED = 'INCREASED'
    UNKNOWN = 'UNKNOWN'


class CreateDeposit(BaseModel):
    coin: str | None
    network: str
    amount: str | None
    decimals: int | None
    confirmation: int
    status: int
    tx_id: str
    memo: str | None
    wallet_address: str | None

    system_status: SystemStatusEnum = SystemStatusEnum.REGISTERED


class UpdateDeposit(BaseModel):
    status: int | None
    system_status: SystemStatusEnum | None
    coin: str | None
    amount: str | None
    decimals: int | None
    confirmation: int | None
    wallet_address: str | None


class GetMultiDeposit(GetMultiBaseModel):
    status: int | None
    system_status: SystemStatusEnum | None
    tx_id: str | None
    wallet_address: str | None
    memo: str | None
    coin: str | None
