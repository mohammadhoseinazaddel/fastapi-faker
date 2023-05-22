from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy import Text

from system.base.crud import CRUDBase
from system.dbs.models import Base
from ..models.schemas.bank_pay import CreateBankPayment, UpdateBankPayment, GetMultiFinBankPayment


class FncBankPayment(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    bank_payment_id = Column(Integer, ForeignKey('fnc_bank_payment.id'), nullable=True)

    type = Column(String, )  # pay_order, installment_pay, ..., reverse, refund
    input_type = Column(String, nullable=False)
    input_unique_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    wage = Column(Integer, default=0, )
    description = Column(Text, )
    expired_at = Column(DateTime, )
    status = Column(String)

    success_pgw_id = Column(Integer, ForeignKey('fnc_payment_gateway.id'), nullable=True)


class BankPaymentCRUD(
    CRUDBase[
        FncBankPayment,
        CreateBankPayment,
        UpdateBankPayment,
        GetMultiFinBankPayment
    ]
):
    pass


bank_pay_crud = BankPaymentCRUD(FncBankPayment)
