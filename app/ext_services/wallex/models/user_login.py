import uuid

from sqlalchemy import Column, Integer, String, DateTime

from system.base.crud import CRUDBase
from system.dbs.models import Base
from .schemas.user_login import UpdateWallexLogin, CreateWallexLogin, GetMultiUsrWlxState


class WlxLogin(Base):
    id = Column(Integer, primary_key=True, nullable=False)

    order_uuid = Column(String)

    state = Column(String, index=True, default=uuid.uuid4)
    wallex_login_url = Column(String(1024))
    code = Column(String, index=True, )
    access_token = Column(String)
    refresh_token = Column(String)
    expire_in = Column(String)
    wallex_user_id = Column(String)
    kyc_level = Column(Integer)

    user_id = Column(Integer)
    wallpay_error = Column(String)

    used_at = Column(DateTime)


class WlxLoginCRUD(CRUDBase[WlxLogin, CreateWallexLogin, UpdateWallexLogin, GetMultiUsrWlxState]):
    pass


wallex_user_crud = WlxLoginCRUD(WlxLogin)
