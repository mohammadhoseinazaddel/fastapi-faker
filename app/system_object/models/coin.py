from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.dialects.postgresql import JSON

from system.base.crud import CRUDBase
from system.dbs.models import Base
from .schemas.coin import CreateCoin, UpdateCoin, GetCoinMulti


class SoCoin(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    name = Column(String, unique=True)
    fa_name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    wallex_symbol = Column(String, nullable=True)

    ltv = Column(Float, nullable=True)
    price_in_rial = Column(Float, nullable=True)
    price_in_usdt = Column(Float, nullable=True)

    logo_address = Column(String(1024))

    networks = Column(JSON, )


class CoinCRUD(CRUDBase[SoCoin, CreateCoin, UpdateCoin, GetCoinMulti]):
    pass


coins_crud = CoinCRUD(SoCoin)
