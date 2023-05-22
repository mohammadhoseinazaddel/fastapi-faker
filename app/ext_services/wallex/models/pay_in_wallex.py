import uuid

from sqlalchemy import Column, Integer, String, JSON

from system.base.crud import CRUDBase
from system.dbs.models import Base
from .schemas.pay_in_wallex import CreateWallexPay, UpdateWallexPay, GetMultiWallexPay


class WlxPayIn(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    token = Column(String, index=True)

    # CREATED - UNVERIFIED - CONFIRMED - REJECTED_BY_USER - REJECTED_BY_SYSTEM
    status = Column(String, nullable=False)
    uuid = Column(String, index=True, default=uuid.uuid4)

    input_type = Column(String, nullable=False)  # example --> OrdOrderID
    input_unique_id = Column(Integer, nullable=False)  # external model transaction id

    assets = Column(JSON, nullable=False)
    redirect_url = Column(String)
    callback_url = Column(String)
    wallex_user_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    state = Column(String)


class WlxPayCRUD(CRUDBase[WlxPayIn, CreateWallexPay, UpdateWallexPay, GetMultiWallexPay]):
    pass


wallex_pay_crud = WlxPayCRUD(WlxPayIn)
