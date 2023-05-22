from typing import Optional

from pydantic import BaseModel, PositiveFloat

from system.base.schema import GetMultiBaseModel


class CreateCryptoWithdraw(BaseModel):
    user_id: int
    unique_id: int | None
    wallet_address_id: int

    from_address: Optional[str]
    from_memo: str | None
    to_address: str
    to_memo: str | None
    amount: PositiveFloat

    status: str | None


class UpdateCryptoWithdraw(BaseModel):
    ack: int | None
    verify: int | None
    bundle_id: int | None
    is_identical: int | None
    fee: float | None
    tx_id: str | None
    status: str | None
    unique_id: int | None


class GetMultiCryptoWithdraw(GetMultiBaseModel):
    user_id: int | None
    wallet_address_id: int | None

    from_address: Optional[str]
    from_memo: str | None
    to_address: str | None
    status: str | None
    ack: int | None
    verify: int | None
    bundle_id: int | None
    is_identical: int | None
    fee: float | None
    tx_id: str | None
    unique_id: int | None
