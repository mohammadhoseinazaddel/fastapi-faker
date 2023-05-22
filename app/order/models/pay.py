import datetime
from typing import Type

from sqlalchemy import Column, Integer, String, DateTime, Float, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Session, relationship

from system.base.crud import CRUDBase, ModelType
from system.dbs.models import Base
from .commission import OrdCommission
from ..models.schemas.pay import GetMultiOrdPay, CreatePayOrderSchema, UpdatePayOrder

class OrdPay(Base):
    title = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    identifier = Column(String, nullable=False)  # Use this field just like temp-token
    user_id = Column(Integer, nullable=True)

    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String)
    action = Column(String)
    paid_at = Column(DateTime, nullable=True)

    merchant_order_id = Column(String, nullable=False)
    merchant_id = Column(Integer, nullable=False)
    merchant_user_id = Column(String, index=True, nullable=False)
    merchant_redirect_url = Column(String, nullable=False)

    settle_id = Column(Integer, nullable=True)
    commission_id = Column(Integer, ForeignKey(OrdCommission.id), nullable=False)
    
    commission = relationship('OrdCommission')

    __table_args__ = (UniqueConstraint('merchant_order_id', 'merchant_id', name='merchant_order'),)


class OrderCRUD(CRUDBase[OrdPay, CreatePayOrderSchema, UpdatePayOrder, GetMultiOrdPay]):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)
        self.STATUS_SUCCESS = 'SUCCESS'
        self.STATUS_FAIL = 'FAIL'
        self.STATUS_FAIL_FILL = 'FAIL_FILL'
        self.STATUS_FAIL_WALLEX = 'FAIL_WALLEX'
        self.STATUS_FAIL_PAYMENT = 'FAIL_PAYMENT'
        self.STATUS_WAIT_PROCESS = 'WAIT_PROCESS'
        self.STATUS_WAIT_WALLEX = 'WAIT_WALLEX'
        self.STATUS_WAIT_PAYMENT = 'WAIT_PAYMENT'
        self.STATUS_WAIT_COLLATERAL = 'WAIT_COLLATERAL'
        self.STATUS_PROCESS = 'PROCESS'
        self.ACTION_UNVERIFIED = 'UNVERIFIED'
        self.ACTION_APPROVED = 'APPROVED'
        self.ACTION_REJECTED = 'REJECTED'
        self.TYPE_POST_PAY = 'POST_PAY'
        self.TYPE_PAY_IN_FOUR = 'PAY_IN_FOUR'
        self.STATUS_REFUNDED = 'REFUNDED'
        self.STATUS_WAIT_IBAN_TO_REFUND = 'WAIT_IBAN_TO_REFUND'
        self.STATUS_REFUNDING = "REFUNDING"


    # Admin panel
    def get_all_pay_orders(
            self,
            db: Session,
            limit: int,
            skip: int,
            order_status: str,
            phone_number: str = None,
            created_at_ge: datetime.datetime = None,
            created_at_le: datetime.datetime = None,
            order_price_ge: int = None,
            order_price_le: int = None,
    ):
        from order.models.fund import OrdFund
        from sqlalchemy.sql import func
        if order_status == self.STATUS_SUCCESS:

            # sum methods
            sum_query_for_paid_amount = \
                func.sum(OrdFund.extra_money_to_pay + OrdFund.repaid_non_free_credit + OrdFund.repaid_free_credit) \
                    .label("paid_amount")
            sum_query_for_remain_amount = \
                func.sum(OrdPay.amount - (
                        OrdFund.extra_money_to_pay + OrdFund.repaid_non_free_credit + OrdFund.repaid_free_credit)) \
                    .label("remain_amount")

            query = db.query(
                self.model,
                UsrUser.mobile,
                OrdFund.payment_id,
                sum_query_for_paid_amount,
                sum_query_for_remain_amount,
            )
            query = query.filter(OrdPay.status == self.STATUS_SUCCESS)
            query = query.join(UsrUser, self.model.user_id == UsrUser.id)
            query = query.join(OrdFund, self.model.id == OrdFund.order_id)
            query = query.group_by(self.model, UsrUser.mobile, OrdFund.id)

            if phone_number:
                query = query.filter(UsrUser.mobile == phone_number)
            if created_at_ge:
                query = query.filter(self.model.created_at >= created_at_ge)
            if created_at_le:
                query = query.filter(self.model.created_at <= created_at_le)
            if order_price_ge:
                query = query.filter(self.model.amount >= order_price_ge)
            if order_price_le:
                query = query.filter(self.model.amount <= order_price_le)
            total_count = query.count()
            query = query.offset(skip).limit(limit)
            return {"query_result": query.all(), "total_count": total_count}
        if order_status == 'WAIT':

            # sum methods
            sum_query_for_paid_amount = \
                func.sum(0) \
                    .label("paid_amount")
            # in 'wait' statuses, extra pay is not paid yet
            sum_query_for_remain_amount = \
                func.sum(0) \
                    .label("remain_amount")

            query = db.query(
                self.model,
                UsrUser.mobile,
                # OrdFund.payment_id,
                sum_query_for_paid_amount,
                sum_query_for_remain_amount,
            )
            query = query.filter(OrdPay.status.contains('WAIT'))
            query = query.join(UsrUser, self.model.user_id == UsrUser.id)
            query = query.join(OrdFund, self.model.id == OrdFund.order_id)
            query = query.group_by(
                self.model,
                UsrUser.mobile,
                # OrdFund.id
            )

            if phone_number:
                query = query.filter(UsrUser.mobile == phone_number)
            if created_at_ge:
                query = query.filter(self.model.created_at >= created_at_ge)
            if created_at_le:
                query = query.filter(self.model.created_at <= created_at_le)
            if order_price_ge:
                query = query.filter(self.model.amount >= order_price_ge)
            if order_price_le:
                query = query.filter(self.model.amount <= order_price_le)

            total_count = query.count()
            query = query.offset(skip).limit(limit)
            return {"query_result": query.all(), "total_count": total_count}
        if order_status == self.STATUS_FAIL:
            # sum methods
            sum_query_for_paid_amount = \
                func.sum(0) \
                    .label("paid_amount")
            # in 'wait' statuses, extra pay is not paid yet
            sum_query_for_remain_amount = \
                func.sum(0) \
                    .label("remain_amount")

            query = db.query(
                self.model,
                UsrUser.mobile,
                OrdFund.payment_id,
                sum_query_for_paid_amount,
                sum_query_for_remain_amount,
            )
            query = query.filter(OrdPay.status.contains('FAIL'))
            query = query.join(UsrUser, self.model.user_id == UsrUser.id)
            query = query.join(OrdFund, self.model.id == OrdFund.order_id)
            query = query.group_by(
                self.model,
                UsrUser.mobile,
                OrdFund.id
            )

            if phone_number:
                query = query.filter(UsrUser.mobile == phone_number)
            if created_at_ge:
                query = query.filter(self.model.created_at >= created_at_ge)
            if created_at_le:
                query = query.filter(self.model.created_at <= created_at_le)
            if order_price_ge:
                query = query.filter(self.model.amount >= order_price_ge)
            if order_price_le:
                query = query.filter(self.model.amount <= order_price_le)

            total_count = query.count()
            query = query.offset(skip).limit(limit)
            return {"query_result": query.all(), "total_count": total_count}
        else:
            raise NotImplemented("order status not implemented")

    def get_all_user_orders(
            self,
            db: Session,
            limit: int,
            skip: int,
            user_id: int,
            created_at_ge: datetime.datetime = None,
            created_at_le: datetime.datetime = None,
            order_price_ge: int = None,
            order_price_le: int = None,
    ):
        from order.models.fund import OrdFund
        from sqlalchemy.sql import func
        sum_query_for_credit_used_amount = \
            func.sum(OrdFund.used_free_credit + OrdFund.used_non_free_credit).label("credit_used_amount")

        query = db.query(
            self.model,
            sum_query_for_credit_used_amount,
            OrdFund.payment_amount
        )
        query = query.join(OrdFund, self.model.id == OrdFund.order_id)
        query = query.group_by(self.model, OrdFund.payment_amount)

        if user_id:
            query = query.filter(self.model.user_id == user_id)
        if created_at_ge:
            query = query.filter(self.model.created_at >= created_at_ge)
        if created_at_le:
            query = query.filter(self.model.created_at <= created_at_le)
        if order_price_ge:
            query = query.filter(self.model.amount >= order_price_ge)
        if order_price_le:
            query = query.filter(self.model.amount <= order_price_le)
        total_count = query.count()
        query = query.offset(skip).limit(limit)
        return {"query_result": query.all(), "total_count": total_count}


pay_crud = OrderCRUD(OrdPay)
