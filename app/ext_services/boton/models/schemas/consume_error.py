from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class CreateConsumeError(BaseModel):
    queue: str
    body: str
    error: str | None


class UpdateConsumeError(BaseModel):
    queue: str | None
    body: str | None
    error: str | None
    status: str | None


class GetMultiConsumeError(GetMultiBaseModel):
    queue: str | None
    body: str | None
    error: str | None
    status: str | None
