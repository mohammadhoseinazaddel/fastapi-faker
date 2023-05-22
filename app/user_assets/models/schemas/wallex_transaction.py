from typing import Literal

from pydantic.main import BaseModel

from system.base.schema import CreateTransactionBaseModel, GetMultiTransactionBaseModel


class CreateWallexTransaction(CreateTransactionBaseModel):
    coin_name: Literal['bitcoin', 'ethereum', 'tether']
    input_type: Literal['fund']


class UpdateWallexTransaction(BaseModel):
    pass


class GetMultiWallexTransaction(GetMultiTransactionBaseModel):
    coin_name: Literal['bitcoin', 'ethereum', 'tether'] | None
