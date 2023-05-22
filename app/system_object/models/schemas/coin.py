import datetime
from typing import Optional, Literal
from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class CreateCoin(BaseModel):
    name: str
    fa_name: str
    symbol: str
    ltv: float
    wallex_symbol: str
    logo_address: str
    networks: dict


class UpdateCoin(BaseModel):
    name: str | None
    fa_name: str | None
    symbol: str | None
    wallex_symbol: str | None
    ltv: float | None
    price_in_rial: float | None
    price_in_usdt: float | None
    deleted_at: datetime.datetime | None


class GetCoinMulti(GetMultiBaseModel):
    id: int | None
    name: str | None
    fa_name: str | None
    symbol: str | None
    wallex_symbol: str | None
    price_in_rial: float | None
    price_in_usdt: float | None
