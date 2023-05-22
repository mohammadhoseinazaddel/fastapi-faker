from sqlalchemy import Column, Integer, String
from system.base.crud import CRUDBase
from system.dbs.models import Base

from .schemas.deposit import CreateDeposit, GetMultiDeposit, UpdateDeposit


class ExtBotonDeposit(Base):
    id = Column(Integer, primary_key=True, nullable=False)

    coin = Column(String)
    network = Column(String, nullable=False)
    amount = Column(String)
    decimals = Column(Integer)
    confirmation = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    tx_id = Column(String, nullable=False)
    memo = Column(String)
    wallet_address = Column(String)

    # System Valid Status Codes : REGISTERED - UPDATED - INCREASED - UNKNOWN
    system_status = Column(String, nullable=False)

    # __table_args__ = (
    #     UniqueConstraint('tx_id', 'wallet_address', 'memo', name='ext_boton_deposit_tx_id__wallet_address__memo'),
    #     Index('ext_boton_deposit_tx_id__wallet_address__memo', "tx_id", "wallet_address", 'memo'),
    # )


class DepositCRUD(CRUDBase[ExtBotonDeposit, CreateDeposit, UpdateDeposit, GetMultiDeposit]):
    pass


deposit_crud = DepositCRUD(ExtBotonDeposit)
