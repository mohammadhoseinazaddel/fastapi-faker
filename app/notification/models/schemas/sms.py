import datetime

from pydantic import BaseModel, Field

from system.base.schema import GetMultiBaseModel


class SmsCreateSchema(BaseModel):
    input_type: str
    input_unique_id: int | None
    status: str = Field(default='READY')
    user_id: int | None
    mobile_number: str
    text: str
    template_id: int | None


class SmsUpdateSchema(BaseModel):
    retried_count: int | None
    last_retried: datetime.datetime | None
    status: str | None
    provider_id: int | None
    provider_name: str | None
    user_id: int | None
    mobile_number: str | None
    text: str | None
    provider_message_id: int | None


class SmsGetMultiSchema(GetMultiBaseModel):
    input_type: str | None
    input_unique_id: str | None
    retried_count: int | None
    status: str | None
    provider_id: int | None
    provider_name: str | None
    user_id: int | None
    mobile_number: str | None
    template_id: int | None
    provider_message_id: int | None
