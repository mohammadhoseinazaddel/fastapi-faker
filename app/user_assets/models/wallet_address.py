from sqlalchemy import Column, Integer, String, UniqueConstraint, Index

from system.base.crud import CRUDBase
from system.dbs.models import Base
from .schemas.wallet_address import CreateUasAddress, UpdateUasAddress, GetMultiUasAddress


class UasWalletAddress(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, )
    national_code = Column(String, nullable=False)
    # only use national_code to query address
    # IMPORTANT: we send national_code as user_id in order to get blockchain address

    coin_name = Column(String, nullable=False)
    network_name = Column(String, nullable=False)
    address = Column(String, unique=True, nullable=False)
    memo = Column(String)

    __table_args__ = (
        UniqueConstraint('national_code', 'coin_name', 'network_name', 'memo', name='uas_wallet_address_unique'),
        Index('uas_wallet_address_index', "national_code", "coin_name", 'network_name'),
    )


class AddressCRUD(CRUDBase[UasWalletAddress, CreateUasAddress, UpdateUasAddress, GetMultiUasAddress]):
    pass


address_crud = AddressCRUD(UasWalletAddress)
