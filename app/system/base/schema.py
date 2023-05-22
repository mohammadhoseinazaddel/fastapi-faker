import datetime
from typing import Literal

from pydantic import BaseModel


class GetMultiBaseModel(BaseModel):
    id: int | None
    deleted_at__isnull: bool = None
    created_at: datetime.datetime | None


class GetMultiTransactionBaseModel(GetMultiBaseModel):
    id: int | None
    input_type: str | None
    input_unique_id: int | None
    type: Literal[
              'increase',
              'decrease',
              'unblock',
              'block',
              'freeze'
          ] | None


class CreateTransactionBaseModel(BaseModel):
    type: Literal['increase', 'decrease', 'block', 'freeze', 'unblock', 'unfreeze']
    user_id: int
    input_unique_id: int
    amount: float
