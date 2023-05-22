from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class CreditUserCreateSchema(BaseModel):
    user_id: int


class CreditUserUpdateSchema(BaseModel):
    is_locked: bool | None


class CreditUserGetMulti(GetMultiBaseModel):
    user_id: int | None
    is_locked: bool | None
