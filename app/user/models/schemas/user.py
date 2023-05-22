from datetime import datetime, date
from pydantic.main import BaseModel


class UserCreateSchema(BaseModel):
    email: str | None
    mobile: str | None
    username: str | None
    hashed_pass: str | None

    first_name: str | None
    last_name: str | None
    father_name: str | None
    gender: str | None
    national_code: str | None
    birth_date: date | None
    profile_image: str | None

    last_login: date | None
    identifier: str | None

    is_disabled: bool | None

    verified: bool | None
    verified_by: str | None
    verified_at: datetime | None

    kyc_id: int | None


class UserUpdateSchema(BaseModel):
    email: str | None
    mobile: str | None
    username: str | None
    hashed_pass: str | None

    first_name: str | None
    last_name: str | None
    father_name: str | None
    gender: str | None
    national_code: str | None
    birth_date: date | None
    profile_image: str | None

    last_login: date | None
    identifier: str | None

    is_disabled: bool | None

    verified: bool | None
    verified_by: str | None
    verified_at: datetime | None

    kyc_id: int | None


class UserGetMultiSchema(BaseModel):
    id: int | None
    email: str | None
    mobile: str | None
    username: str | None
    hashed_pass: str | None

    first_name: str | None
    last_name: str | None
    father_name: str | None
    gender: str | None
    national_code: str | None
    birth_date: date | None
    profile_image: str | None

    last_login: date | None
    identifier: str | None

    is_disabled: bool | None

    verified: bool | None
    verified_by: str | None
    verified_at: datetime | None

    kyc_id: int | None
