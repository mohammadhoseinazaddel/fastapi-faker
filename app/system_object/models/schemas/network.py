import datetime
from typing import Optional, Literal
from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class CreateNetwork(BaseModel):
    name: str


class UpdateNetwork(BaseModel):
    name: str | None


class GetNetworkMulti(GetMultiBaseModel):
    id: int | None
    name: str | None
