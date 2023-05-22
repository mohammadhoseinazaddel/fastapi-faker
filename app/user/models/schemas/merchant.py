from typing import Optional
from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class CreateMerchant(BaseModel):
    name: str
    url: Optional[str]
    logo_address: Optional[str]
    name_fa: Optional[str]
    logo_background_color: str


class UpdateMerchant(BaseModel):
    name: Optional[str]
    url: Optional[str]
    logo_address: Optional[str]
    logo_background_color: str | None
    name_fa: str | None


class GetMultiMerchant(GetMultiBaseModel):
    identifier: str | None
    name: str | None


class GetMerchantByName(BaseModel):
    name: str
