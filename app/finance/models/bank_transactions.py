from sqlalchemy import Column, Integer, String

from finance.models.schemas.bank_transactions import BankTransactionsCreate, BankTransactionsUpdate, \
    BankTransactionsGetMulti
from system.base.crud import CRUDBase
from system.dbs.models import Base


class FncBankTransactions(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)


class BankTransactionsCRUD(
    CRUDBase[
        FncBankTransactions,
        BankTransactionsCreate,
        BankTransactionsUpdate,
        BankTransactionsGetMulti
    ]
):
    pass


bank_transactions_crud = BankTransactionsCRUD(FncBankTransactions)
