import uuid

from sqlalchemy import Column, Integer, String, Date

from finance.models.schemas.debt_user import DebtUserCreate, DebtUserUpdate, DebtUserGetMulti
from system.base.crud import CRUDBase
from system.dbs.models import Base


class FncDebtUser(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    amount = Column(Integer, nullable=False)  # مثبت به معنی بدهی کاربر و منفی به معنی بازپرداخت
    due_date = Column(Date)  # تاریخ سررسید
    order_id = Column(Integer, nullable=False)

    input_type = Column(String)
    input_unique_id = Column(Integer)


class DebtUserCRUD(
    CRUDBase[
        FncDebtUser,
        DebtUserCreate,
        DebtUserUpdate,
        DebtUserGetMulti
    ]
):
    pass


debt_user_crud = DebtUserCRUD(FncDebtUser)
