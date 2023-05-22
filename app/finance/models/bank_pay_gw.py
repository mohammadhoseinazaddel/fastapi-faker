import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, desc
from sqlalchemy.orm import Session

from finance.exceptions.payment_gateway import PaymentGatewayNotFound
from finance.models.bank_pay import FncBankPayment
from finance.models.schemas.bank_pay_gw import CreatePaymentGateway, UpdatePaymentGateway, GetMultiFinPaymentGateway
from system.base.crud import CRUDBase
from system.dbs.models import Base


class FncPaymentGateway(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    type = Column(String, nullable=False)  # pay, reverse, refund
    payment_gateway_id = Column(Integer, ForeignKey('fnc_payment_gateway.id'))

    bank_payment_id = Column(Integer, ForeignKey(FncBankPayment.id))

    amount = Column(Integer, nullable=False)
    wage = Column(Integer, )
    gateway_name = Column(String)
    description = Column(Text, )

    status = Column(String)  # Wallpay Status

    ref_num = Column(String, index=True, default=uuid.uuid4)

    expired_at = Column(DateTime, )

    # psp side
    psp_purchase_id = Column(String)
    psp_switching_url = Column(String(1024))
    callback_status = Column(String)
    psp_status = Column(String, )  # IN_PROGRESS, READY_TO_VERIFY,EXPIRED, FAILED, REVERSED, SUCCESS, and UNKNOWN.
    psp_trace_no = Column(String)
    payer_ip = Column(String)
    psp_ref_num = Column(String)
    psp_rrn = Column(String)
    payer_masked_card_num = Column(String)
    psp_name = Column(String)

    reversed_at = Column(DateTime)
    reverse_status = Column(String)

    refund_batch_id = Column(String)
    refund_transfer_id = Column(String)

    # bank_payment = relationship("FinBankPayment", back_populates="payment_gateway")


class PaymentGatewayCRUD(
    CRUDBase[FncPaymentGateway, CreatePaymentGateway, UpdatePaymentGateway, GetMultiFinPaymentGateway]):

    def find_by_bank_payment_id(self, bank_payment_id: int, db: Session) -> List[FncPaymentGateway]:
        pay_gw_list = db.query(FncPaymentGateway).filter(FncPaymentGateway.bank_payment_id == bank_payment_id).all()
        if not pay_gw_list:
            raise PaymentGatewayNotFound

        return pay_gw_list

    def find_last_by_bank_payment_id(self, bank_payment_id: int, db: Session) -> FncPaymentGateway:
        pay_gw = db.query(FncPaymentGateway).filter(
            FncPaymentGateway.bank_payment_id == bank_payment_id,
            FncPaymentGateway.status != 'FAIL',
            FncPaymentGateway.status != 'SUCCESS',
        ).order_by(desc(FncPaymentGateway.updated_at)).first()

        if not pay_gw:
            raise PaymentGatewayNotFound

        return pay_gw

    def find_by_ref_num(self, ref_num: str, db: Session) -> FncPaymentGateway:
        pay_gw = db.query(FncPaymentGateway).filter(FncPaymentGateway.ref_num == ref_num).first()
        if not pay_gw:
            raise PaymentGatewayNotFound

        return pay_gw

    # Admin panel
    def get_all_payment_gateways(
            self,
            db: Session,
            limit: int,
            skip: int,
            phone_number: str = None,
            created_at_ge: datetime = None,
            created_at_le: datetime = None,
            price_ge: int = None,
            price_le: int = None,
    ):
        from user.models.user_model import UsrUser

        query = db.query(
            self.model.id,
            self.model.amount,
            self.model.type.label('reason'),
            self.model.created_at,
            self.model.gateway_name,
            self.model.status,
            UsrUser.mobile.label('user_phone_number'),
            UsrUser.id.label('user_id')
        )
        query = query.filter(self.model.deleted_at == None)
        query = query.join(FncBankPayment, self.model.bank_payment_id == FncBankPayment.id)
        query = query.join(UsrUser, FncBankPayment.user_id == UsrUser.id)

        if phone_number:
            query = query.filter(UsrUser.mobile == phone_number)
        if created_at_ge:
            query = query.filter(self.model.created_at >= created_at_ge)
        if created_at_le:
            query = query.filter(self.model.created_at <= created_at_le)
        if price_ge:
            query = query.filter(self.model.amount >= price_ge)
        if price_le:
            query = query.filter(self.model.amount <= price_le)

        total_count = query.count()
        query = query.offset(skip).limit(limit)
        return {"query_result": query.all(), "total_count": total_count}


payment_gateway_crud = PaymentGatewayCRUD(FncPaymentGateway)
