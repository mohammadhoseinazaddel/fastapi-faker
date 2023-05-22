
from typing import Literal

from pydantic.main import BaseModel

from system.base.schema import CreateTransactionBaseModel, GetMultiTransactionBaseModel


class CreateFiatTransaction(CreateTransactionBaseModel):
    input_type: Literal['fund', 'withdraw', 'deposit', 'refund']


class UpdateFiatTransaction(BaseModel):
    pass


class GetMultiFiatTransaction(GetMultiTransactionBaseModel):
    pass