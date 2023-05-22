from typing import Optional
from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class CreateRules(BaseModel):
    version: str
    rules: str


class UpdateRules(BaseModel):
    version: str
    rules: str


class GetMultiSoRule(GetMultiBaseModel):
    pass