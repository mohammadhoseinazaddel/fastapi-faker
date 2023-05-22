from datetime import datetime
from pydantic.main import BaseModel


class SessionCreateSchema(BaseModel):
    token: str
    user_id: int
    expire_at: datetime
    token_first_used_at: datetime | None
    token_last_used_at: datetime | None
    is_valid: bool | None

    os: str | None
    os_version: str | None
    browser: str | None
    browser_version: str | None
    ip: str | None


class SessionUpdateSchema(BaseModel):
    token: str | None
    user_id: int | None
    expire_at: datetime | None
    token_last_used_at: datetime | None
    is_valid: bool | None


class SessionGetMultiSchema(BaseModel):
    id: int | None
    token: str | None
    user_id: int | None
    is_valid: bool | None

    os: str | None
    os_version: str | None
    browser: str | None
    browser_version: str | None
    ip: str | None
