from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class ProviderCreateSchema(BaseModel):
    name: str
    line_number: str
    position_number: int


class ProviderUpdateSchema(BaseModel):
    name: str | None
    line_number: str | None
    position_number: int | None


class ProviderGetMultiSchema(GetMultiBaseModel):
    name: str | None
    line_number: str | None
    position_number: int | None
