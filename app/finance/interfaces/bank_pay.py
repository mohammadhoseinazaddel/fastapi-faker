from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.config import settings
from system.dbs.postgre import SessionLocal
from ..exceptions.bank_payment import BankPaymentPaid

from ..models.bank_pay import bank_pay_crud
from ..models.schemas.bank_pay import UpdateBankPayment, CreateBankPayment, GetMultiFinBankPayment


class BankPaymentInterface(InterfaceBase):
    """
    this class work base on safe delete
    """
    PAY_ORDER_BANK_PAYMENT = 'pay_order'
    REPAY_ORDER_BANK_PAYMENT = 'repay_pay_order'
    REVERSE_BANK_PAYMENT = 'reverse'
    REFUND_BANK_PAYMENT = 'refund'

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        from ..exceptions import bank_payment as bank_payment_exceptions
        self.exceptions = bank_payment_exceptions
        self.base_crud = bank_pay_crud

    def send_to_payment_gateway(
            self,
            bank_pay_id: int,
            description: str = 'پرداخت',
            gateway_name: str = 'jibit',
            db: Session = SessionLocal()
    ):
        from .bank_pay_gw import payment_gateway_agent
        from order import OrderService

        from user import UserService
        user_sr = UserService()
        pay_order_sr = OrderService()

        # check if bank pay exists
        bank_pay = self.find_item_multi(
            db=db,
            id=bank_pay_id
        )[0]

        user = user_sr.user.find_item_multi(db=db, user_id=bank_pay.user_id)[0]

        if bank_pay.status == 'PAID':
            raise BankPaymentPaid

        if bank_pay.input_type == 'pay_order':
            order = pay_order_sr.pay.find_item_multi(
                db=db,
                id=bank_pay.input_unique_id
            )[0]
            pay_order_sr.pay.check_order_validity(db=db, uuid=order.identifier)

        res = payment_gateway_agent.get_switching_url(
            bank_payment_id=bank_pay_id,
            gateway_name=gateway_name,
            amount=bank_pay.amount,
            user_identifier=user.identifier,
            user_mobile=user.mobile,
            description=description,
            db=db
        )

        if res['psp_switching_url']:
            self.update_item(
                db=db,
                find_by={'id': bank_pay_id},
                update_to={
                    "status": 'PAYMENT_GATEWAY_PROCESSING',
                }
            )

        return res


bank_pay_agent = BankPaymentInterface(
    crud=bank_pay_crud,
    create_schema=CreateBankPayment,
    update_schema=UpdateBankPayment,
    get_multi_schema=GetMultiFinBankPayment
)
