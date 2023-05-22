from enum import Enum

from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class StatusEnum(str, Enum):
    CREATED = 'CREATED'
    UNVERIFIED = 'UNVERIFIED'
    CONFIRMED = 'CONFIRMED'
    REJECTED_BY_USER = 'REJECTED_BY_USER'
    REJECTED_BY_SYSTEM = 'REJECTED_BY_SYSTEM'


class CreateWallexPay(BaseModel):
    status: StatusEnum = StatusEnum.CREATED
    input_type: str
    input_unique_id: int
    assets: list
    wallex_user_id: int
    user_id: int


class UpdateWallexPay(BaseModel):
    token: str | None
    status: StatusEnum | None
    state: str | None
    callback_url: str | None
    redirect_url: str | None


class GetMultiWallexPay(GetMultiBaseModel):
    token: str | None
    status: StatusEnum | None
    uuid: str | None
    input_type: str | None
    input_unique_id: int | None
    user_id: int | None
    wallex_user_id: int | None
    callback_type: str | None
