from typing import Optional, List
from datetime import datetime
from pydantic.main import BaseModel


class UserMerchantsCreateSchema(BaseModel):
    user_id: int
    merchant_id: int


class UserMerchantsUpdateSchema(BaseModel):
    pass


class UserMerchantsGetMultiSchema(BaseModel):
    user_id: int | None
    merchant_id: int | None

