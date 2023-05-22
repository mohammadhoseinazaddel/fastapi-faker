from typing import Literal

from pydantic.main import BaseModel

from system.base.schema import CreateTransactionBaseModel, GetMultiTransactionBaseModel


class CreateCryptoTransaction(CreateTransactionBaseModel):
    coin_name: Literal['bitcoin', 'ethereum', 'tether']
    input_type: Literal['fund', 'withdraw', 'deposit']


class UpdateCryptoTransaction(BaseModel):
    pass


class GetMultiCryptoTransaction(GetMultiTransactionBaseModel):
    coin_name: Literal['bitcoin', 'ethereum', 'tether'] | None
