from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from finance.models.schemas.refund import RefundCreate, RefundUpdate, RefundGetMulti
from system.base.crud import CRUDBase
from system.dbs.models import Base


class FncRefund(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    uuid = Column(String, unique=True)

    order_id = Column(Integer, nullable=False, unique=True)
    order_uuid = Column(String, nullable=False, unique=True)
    order_user_id = Column(Integer, nullable=False)
    status = Column(String, nullable=False)  # REQUESTED_FROM_MERCHANT, DONE

    merchant_id = Column(Integer, nullable=False, index=True)
    merchant_user_id = Column(Integer, nullable=False)  # merchant admin user who requested refund
    amount = Column(Integer, nullable=False)

    # user has been refunded with his debt it means we decrease his debt
    refund_by_debt = Column(Integer, nullable=True)
    # rial amount that we transferred him directly by "paya"
    refund_by_rial = Column(Integer, nullable=True)


class RefundCRUD(
    CRUDBase[
        FncRefund,
        RefundCreate,
        RefundUpdate,
        RefundGetMulti
    ]
):
    pass


refund_crud = RefundCRUD(FncRefund)
