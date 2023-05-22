from pydantic import BaseModel, Field

from system.base.schema import GetMultiBaseModel


class PushNotificationCreateSchema(BaseModel):
    input_type: str
    input_unique_id: int
    status: str = Field(default='READY')
    title: str
    user_id: int | None
    token: str
    text: str
    template_id: int | None


class PushNotificationUpdateSchema(BaseModel):
    status: str | None
    user_id: int | None
    token: str | None
    text: str | None


class PushNotificationGetMultiSchema(GetMultiBaseModel):
    input_type: str | None
    input_unique_id: str | None
    title: str | None
    status: str | None
    user_id: int | None
    token: str | None
    template_id: int | None
