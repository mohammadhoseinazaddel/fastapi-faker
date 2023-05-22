from sqlalchemy import Column, Integer, String

from system.base.crud import CRUDBase
from system.dbs.models import Base, TransactionModelFields
from ..models.schemas.wallex_transaction import \
    CreateWallexTransaction, \
    UpdateWallexTransaction, \
    GetMultiWallexTransaction


class UasWallexTransaction(Base, TransactionModelFields):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    coin_name = Column(String, nullable=False)


class WallexTransactionCRUD(
    CRUDBase[
        UasWallexTransaction,
        CreateWallexTransaction,
        UpdateWallexTransaction,
        GetMultiWallexTransaction,
    ]
):
    pass


wallex_transaction_crud = WallexTransactionCRUD(UasWallexTransaction)
