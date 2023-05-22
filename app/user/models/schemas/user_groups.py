from typing import Optional, List
from datetime import datetime
from pydantic.main import BaseModel


class UserGroupsCreateSchema(BaseModel):
    user_id: int
    group_id: int


class UserGroupsUpdateSchema(BaseModel):
    pass


class UserGroupsGetMultiSchema(BaseModel):
    user_id: int | None
    group_id: int | None

