from typing import Any, Optional, List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, relationship

from system.base.crud import CRUDBase
from system.dbs.models import Base
from .user_merchants import user_merchants
from ..exceptions.merchant import MerchantNotFound
from ..models.schemas.merchant import CreateMerchant, UpdateMerchant, GetMultiMerchant, GetMerchantByName


class UsrMerchant(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, unique=True, nullable=False)
    name_fa = Column(String, unique=True, nullable=False)
    url = Column(String(1024), )
    logo_address = Column(String(1024))
    logo_background_color = Column(String(128))
    
    user = relationship(
        'UsrUser', secondary=user_merchants, uselist=False, back_populates="merchant"
    )


class MerchantCRUD(CRUDBase[UsrMerchant, CreateMerchant, UpdateMerchant, GetMultiMerchant]):
    def get_by_name(self, db: Session, obj_in: GetMerchantByName) -> Optional[UsrMerchant]:
        return db.query(self.model).filter(self.model.name == obj_in.name).first()


merchant_crud = MerchantCRUD(UsrMerchant)
