from typing import Literal

from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class BankTransactionsCreate(BaseModel):
    pass


class BankTransactionsUpdate(BaseModel):
    pass


class BankTransactionsGetMulti(GetMultiBaseModel):
    pass
