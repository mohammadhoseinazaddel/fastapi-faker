from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint, Table

from system.base.crud import CRUDBase
from system.dbs.models import Base
from user.models.schemas.user_merchants import UserMerchantsCreateSchema, UserMerchantsUpdateSchema, UserMerchantsGetMultiSchema


class UsrUserMerchants(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    user_id = Column(Integer, ForeignKey('usr_user.id'), nullable=False)
    merchant_id = Column(Integer, ForeignKey('usr_merchant.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'merchant_id', name='user_merchant_unique'),
    )
    
user_merchants = Table(
    UsrUserMerchants.__tablename__,
    Base.metadata,
    Column("user_id", ForeignKey('usr_user.id'), nullable=False),
    Column("merchant_id", ForeignKey('usr_merchant.id'), nullable=False),
    extend_existing=True
)

class UserMerchantsCRUD(
    CRUDBase[
        UsrUserMerchants,
        UserMerchantsCreateSchema,
        UserMerchantsUpdateSchema,
        UserMerchantsGetMultiSchema
    ]
):
    pass


user_merchants_crud = UserMerchantsCRUD(UsrUserMerchants)
