import datetime

from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index

from finance.models.schemas.settle_credit import SettleCreditCreate, SettleCreditUpdate, SettleCreditGetMulti
from finance.models.transfer import FncTransfer
from system.base.crud import CRUDBase, ModelType
from system.dbs.models import Base
from typing import Type


class FncSettleCredit(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    order_id = Column(Integer, index=True)
    order_uuid = Column(String, index=True)
    type = Column(String, nullable=False)  # pay, reverse, refund

    merchant_id = Column(Integer, nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    transfer_id = Column(Integer, ForeignKey(FncTransfer.id), nullable=True)

    __table_args__ = (
        UniqueConstraint('order_id', 'type', name='FncSettleCredit_fnc_order.id__type'),
        Index('FncSettleCredit_fnc_order_id__type', "order_id", "type"),
    )


class SettleCreditCRUD(
    CRUDBase[
        FncSettleCredit,
        SettleCreditCreate,
        SettleCreditUpdate,
        SettleCreditGetMulti
    ]
):

    def __init__(self, model: Type[ModelType]):
        super().__init__(model)

    def get_credit_settle_detail(
            self,
            db: Session,
            limit: int,
            skip: int,
            created_at_ge: datetime.datetime = None,
            created_at_le: datetime.datetime = None,
            transfer_price_ge: float = None,
            transfer_price_le: float = None,
            merchant_id: int = None,
            transfer_id: int = None,
            settlement_id: int = None,
            order_id: int = None,
            order_uuid: str = None,
            unsettled: bool = None,
    ):

        query = db.query(
            self.model,
        )
        if merchant_id:
            query = query.filter(self.model.merchant_id == merchant_id)
        if unsettled:
            query = query.filter(self.model.transfer_id == None)
        if transfer_id:
            query = query.filter(self.model.transfer_id == transfer_id)
        if settlement_id:
            query = query.filter(self.model.id == settlement_id)
        if order_id:
            query = query.filter(self.model.order_id == order_id)
        if order_uuid:
            query = query.filter(self.model.order_uuid == order_uuid)
        if created_at_ge:
            query = query.filter(self.model.created_at >= created_at_ge)
        if created_at_le:
            query = query.filter(self.model.created_at <= created_at_le)
        if transfer_price_ge:
            query = query.filter(self.model.amount >= transfer_price_ge)
        if transfer_price_le:
            query = query.filter(self.model.amount <= transfer_price_le)

        total_count = query.count()
        query = query.offset(skip).limit(limit)
        return {"query_result": query.all(), "total_count": total_count}


settle_credit_crud = SettleCreditCRUD(FncSettleCredit)
