from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class TemplateCreateSchema(BaseModel):
    name: str
    text: str
    title: str


class TemplateUpdateSchema(BaseModel):
    name: str | None
    text: str | None
    title: str | None


class TemplateGetMultiSchema(GetMultiBaseModel):
    name: str | None