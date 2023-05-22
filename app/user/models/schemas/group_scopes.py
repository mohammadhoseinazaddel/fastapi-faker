from typing import Optional, List
from datetime import datetime
from pydantic.main import BaseModel


class GroupScopesCreateSchema(BaseModel):
    group_id: int
    scope_id: int


class GroupScopesUpdateSchema(BaseModel):
    pass


class GroupScopesGetMultiSchema(BaseModel):
    group_id: int | None
    scope_id: int | None

