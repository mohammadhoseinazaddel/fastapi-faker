
from pydantic.main import BaseModel


class GroupCreateSchema(BaseModel):
    name: str
    fa_name: str | None
    description: str | None


class GroupUpdateSchema(BaseModel):
    fa_name: str | None
    description: str | None


class GroupGetMultiSchema(BaseModel):
    name: str | None

