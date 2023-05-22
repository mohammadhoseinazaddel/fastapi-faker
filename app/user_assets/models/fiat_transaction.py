from sqlalchemy import Column, Integer

from system.base.crud import CRUDBase
from system.dbs.models import Base, TransactionModelFields
from .schemas.fiat_transaction import CreateFiatTransaction, UpdateFiatTransaction, GetMultiFiatTransaction


class UasFiatTransaction(Base, TransactionModelFields):
    id = Column(Integer, primary_key=True, index=True, nullable=False)


class FiatTransactionCRUD(
    CRUDBase[
        UasFiatTransaction,
        CreateFiatTransaction,
        UpdateFiatTransaction,
        GetMultiFiatTransaction,
    ]
):
    pass


fiat_transaction_crud = FiatTransactionCRUD(UasFiatTransaction)
