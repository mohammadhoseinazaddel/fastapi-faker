from sqlalchemy import Column, Integer, String, Float, Boolean, Index

from system.base.crud import CRUDBase
from system.dbs.models import Base
from .schemas.commission import CreateCommission, UpdateCommission, GetMultiCommission


class OrdCommission(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    merchant_id = Column(Integer, nullable=False)
    category = Column(String, nullable=False)

    pgw_commission_constant = Column(Integer, nullable=False, default=0)
    pgw_commission_rate = Column(Float, nullable=False, default=0)
    pgw_fee_constant = Column(Integer, default=0)
    pgw_fee_rate = Column(Float, default=0)

    credit_commission_constant = Column(Integer, nullable=False, default=0)
    credit_commission_rate = Column(Float, nullable=False, default=0)
    credit_limit = Column(Integer, nullable=False, default=0)   # سقف اعتبار

    decrease_fee_on_pay_gw_settle = Column(Boolean, default=True)
    decrease_commission_on_refund = Column(Boolean, default=True)

    __table_args__ = (
        Index("merchant_id", "category"),
    )


class CommissionCRUD(
    CRUDBase[
        OrdCommission,
        CreateCommission,
        UpdateCommission,
        GetMultiCommission]
):
    pass


commission_crud = CommissionCRUD(OrdCommission)
