from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class CreateWallexLogin(BaseModel):
    order_uuid: str | None


class UpdateWallexLogin(BaseModel):
    code: str | None
    wallex_login_url: str | None
    access_token: str | None
    refresh_token: str | None
    expire_in: int | None
    wallex_user_id: str | None
    kyc_level: int | None
    user_id: int | None
    wallpay_error: str | None


class GetMultiUsrWlxState(GetMultiBaseModel):
    id: int | None
    state: str | None
    code: str | None
    wallex_user_id: str | None
    kyc_level: int | None
    user_id: int | None
    wallpay_error: str | None
    access_token: str | None

