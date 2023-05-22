from datetime import datetime

from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.dbs.postgre import SessionLocal

from finance.models.bank_transactions import bank_transactions_crud
from finance.models.schemas.bank_transactions import BankTransactionsCreate, BankTransactionsUpdate, \
    BankTransactionsGetMulti


class BankTransactionsInterface(InterfaceBase):

    def __init__(
            self,
            crud: CRUDBase,
            create_schema,
            update_schema,
            get_multi_schema
    ):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = bank_transactions_crud


bank_transactions_agent = BankTransactionsInterface(
    crud=bank_transactions_crud,
    create_schema=BankTransactionsCreate,
    update_schema=BankTransactionsUpdate,
    get_multi_schema=BankTransactionsGetMulti
)
