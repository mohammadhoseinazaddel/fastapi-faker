from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class CreateUasAddress(BaseModel):
    user_id: int
    national_code: str
    coin_name: str
    network_name: str
    address: str


class UpdateUasAddress(BaseModel):
    coin_name: str
    network_name: str
    address: str


class GetUasAddressInput(BaseModel):
    user_id: int
    coin_name: str
    network_name: str


class GetUasAddressByWallet(BaseModel):
    address: str


class GetMultiUasAddress(GetMultiBaseModel):
    user_id: int | None
    national_code: str | None
    coin_name: str | None
    network_name: str | None
    address: str | None
    memo: str | None

