from sqlalchemy import Column, String, Integer

from system.base.crud import CRUDBase
from system.dbs.models import Base, TransactionModelFields
from .schemas.crypto_transaction import CreateCryptoTransaction, \
    UpdateCryptoTransaction, GetMultiCryptoTransaction


class UasCryptoTransaction(Base, TransactionModelFields):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    coin_name = Column(String, nullable=False)


class CryptoTransactionCRUD(
    CRUDBase[
        UasCryptoTransaction,
        CreateCryptoTransaction,
        UpdateCryptoTransaction,
        GetMultiCryptoTransaction,
    ]
):
    pass


crypto_transaction_crud = CryptoTransactionCRUD(UasCryptoTransaction)
