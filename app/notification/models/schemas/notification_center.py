from pydantic import BaseModel
from system.base.schema import GetMultiBaseModel


class NotificationCenterCreateSchema(BaseModel):
    input_type: str | None
    input_unique_id: int | None
    title: str | None
    user_id: int | None
    text: str
    template_id: int | None
    with_sms: bool | None
    with_push_notification: bool | None


class NotificationCenterUpdateSchema(BaseModel):
    pass


class NotificationCenterGetMultiSchema(GetMultiBaseModel):
    with_push_notification: bool | None
    user_id: int
    seen_at__isnull: bool | None
