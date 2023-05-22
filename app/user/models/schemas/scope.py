from typing import Optional, List
from datetime import datetime
from pydantic.main import BaseModel


class ScopeCreateSchema(BaseModel):
    name: str
    fa_name: str | None
    description: str | None
    module: str | None
    interface: str | None
    endpoint: str | None
    action: str | None


class ScopeUpdateSchema(BaseModel):
    name: str | None
    fa_name: str | None
    description: str | None
    module: str | None
    interface: str | None
    endpoint: str | None
    action: str | None


class ScopeGetMultiSchema(BaseModel):
    name: str | None
    fa_name: str | None
    description: str | None
    module: str | None
    interface: str | None
    endpoint: str | None
    action: str | None

