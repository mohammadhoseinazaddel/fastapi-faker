from sqlalchemy import Column, Integer, Boolean

from credit.models.schemas.user import CreditUserCreateSchema, CreditUserUpdateSchema, CreditUserGetMulti
from system.base.crud import CRUDBase
from system.dbs.models import Base


class CrdUser(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=False, unique=True)
    is_locked = Column(Boolean, default=False)


class CreditUserCRUD(
    CRUDBase[
        CrdUser,
        CreditUserCreateSchema,
        CreditUserUpdateSchema,
        CreditUserGetMulti]
):
    pass


credit_user_crud = CreditUserCRUD(CrdUser)
