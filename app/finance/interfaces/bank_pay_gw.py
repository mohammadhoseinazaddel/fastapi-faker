import datetime
import time
from typing import List

from sqlalchemy.orm import Session

from ext_services.jibit.interfaces.payment_gateway import jibit_payment_gw_agent
from system.base.exceptions import HTTP_401_Walpay
from system.base.interface import InterfaceBase
from system.config import settings
from system.dbs.postgre import SessionLocal
from user.interfaces.user import UserInterface
from ..exceptions.payment_gateway import PaymentGatewayNotGetPurchaseId, PaymentGatewayNotFound
from ..models.bank_pay_gw import payment_gateway_crud, FncPaymentGateway
from ..models.schemas.bank_pay_gw import CreatePaymentGateway, UpdatePaymentGateway, GetMultiFinPaymentGateway, \
    CqGetAllPaymentGateways


class PaymentGatewayInterface(InterfaceBase):
    # use jibit_paymnt_gw_agent
    from system.base.crud import CRUDBase

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = payment_gateway_crud

    def get_switching_url(
            self,
            bank_payment_id: int,
            description: str = None,
            db: Session = SessionLocal(),
            gateway_name: str = 'jibit',
    ):
        try:
            from finance import FinanceService
            from order import OrderService
            from user import UserService

            finance_sr = FinanceService()
            user_sr = UserService()
            bank_pay = finance_sr.bank.payment.find_item_multi(
                db=db,
                id=bank_payment_id
            )[0]

            user = user_sr.user.find_item_multi(db=db, id=bank_pay.user_id)[0]
            # create payment_gateway record
            pay_gw = self.add_item(
                db=db,
                type='pay',
                bank_payment_id=bank_payment_id,
                amount=bank_pay.amount,
                gateway_name=gateway_name,
                description=description
            )
            db.add(pay_gw)
            db.commit()

            # send to jibit payment gateway
            res = jibit_payment_gw_agent.create_purchase(
                purchase_ref_num=str(pay_gw.ref_num),
                amount=pay_gw.amount,
                description=pay_gw.description,
                user_identifier=user.identifier,
                user_mobile_num=user.mobile,
                wage=0,
                callback_url=settings.JIBIT_PAY_GW_CALLBACK_BASE_URL + '/' + str(
                    pay_gw.ref_num) + '/' + 'jibit_pay_gw_callback'
            )

            self.update_item(
                db=db,
                find_by={'id': pay_gw.id},
                update_to={
                    "status": 'SENT',
                    "psp_purchase_id": str(res['psp_purchase_id']),
                    "psp_switching_url": res['psp_switching_url']

                }
            )

            db.add(pay_gw)
            db.commit()

            return {
                'payment_gateway_record': pay_gw,
                'psp_switching_url': res['psp_switching_url']
            }

        except Exception as e:
            db.rollback()  # maybe it is extra in this specific case
            raise e

    def callback(
            self,
            ref_num: str,
            amount: int,
            psp_purchase_id: str,
            wage: int,
            payer_ip: str,
            callback_status: str,
            psp_ref_num: str,
            payer_masked_card_num: str,
            psp_rrn: str,
            psp_name: str,
            db: Session
    ) -> FncPaymentGateway:
        try:
            from order import OrderService

            # check if payment_gateway.ref_num does not exist raise 401 (the only authentication way)
            pay_gateway = self.validate_pay_gw_by_ref_num(ref_num=ref_num, db=db)

            # update payment_gateway record
            self.update_item(
                db=db,
                find_by={'id': pay_gateway.id},
                update_to={
                    "payer_ip": payer_ip,
                    "callback_status": callback_status,
                    "psp_ref_num": psp_ref_num,
                    "payer_masked_card_num": payer_masked_card_num,
                    "psp_rrn": psp_rrn,
                    "psp_name": psp_name,
                }
            )
            db.commit()

            # verify purchase based on callback_status
            payment_is_successful = False
            if callback_status == 'SUCCESSFUL':
                pay_gateway = self.verify_purchase(payment_gateway_id=pay_gateway.id, db=db)
                """
                verify purchase status list:
                    SUCCESSFUL
                    ALREADY_VERIFIED
                    FAILED
                    REVERSED
                    NOT_VERIFIABLE
                    UNKNOWN
                reference: https://napi.jibit.ir/ppg/v3/static/docs/index.html#_verificationresultdto
                """
                # decision-making based on verification status
                if pay_gateway.psp_status in ['UNKNOWN']:
                    # pay_gateway must be inquired
                    for i in range(3):
                        pay_gateway = self.inquiry_psp_status_from_pgp(payment_gateway_id=pay_gateway.id, db=db)
                        time.sleep(0.01)
                        if pay_gateway.psp_status != 'UNKNOWN':
                            break
                    if pay_gateway.psp_status == 'UNKNOWN':
                        payment_is_successful = False

                if pay_gateway.psp_status in ['SUCCESS', 'SUCCESSFUL', 'ALREADY_VERIFIED']:
                    # purchase is verified
                    payment_is_successful = True

                elif pay_gateway.psp_status in ['FAILED', 'REVERSED', 'NOT_VERIFIABLE']:
                    # purchase is not verified
                    payment_is_successful = False

            elif callback_status == 'FAILED':
                payment_is_successful = False

            self.update_item(
                db=db,
                find_by={'id': pay_gateway.id},
                update_to={'status': "SUCCESS" if payment_is_successful else 'FAIL'}
            )
            db.commit()

            return pay_gateway

        except Exception as e:
            db.rollback()
            raise e

    def verify_purchase(self, payment_gateway_id, db: Session = SessionLocal()):
        try:
            pay_gw = self.crud.get(db=db, id=payment_gateway_id)
            if pay_gw.psp_purchase_id is None:
                raise PaymentGatewayNotGetPurchaseId

            res = jibit_payment_gw_agent.verify_purcahse(pay_gw.psp_purchase_id)

            pay_gw.psp_status = res["psp_status"]
            db.add(pay_gw)
            # pay_gw = self.crud.update(
            #     db=db,
            #     db_obj=pay_gw,
            #     obj_in=UpdatePaymentGateway(
            #         psp_status=res["psp_status"]
            #     )
            # )
            return pay_gw

        except Exception as e:
            db.rollback()  # maybe it is extra in this specific case
            raise e

    def reverse_purchase(
            self,
            previous_payment_gateway_id: int,
            bank_payment_id: int,
            db: Session
    ) -> FncPaymentGateway:
        from ..finance_service import FinanceService
        finance_sr = FinanceService()
        previous_payment_gateway = self.crud.get(db=db, id=previous_payment_gateway_id)
        previous_bank_payment = finance_sr.bank.payment.crud.get(db=db, id=previous_payment_gateway.bank_payment_id)
        bank_payment = finance_sr.bank.payment.crud.get(db=db, id=bank_payment_id)

        if previous_bank_payment.status != 'PAID':
            raise SystemError(f"bank payment id {previous_bank_payment.id} is not PAID, so it is not reversible")

        payment_gateway = finance_sr.bank.gateway.add_item(
            db=db,
            type='reverse',
            bank_payment_id=bank_payment_id,
            amount=bank_payment.amount,
            gateway_name=previous_payment_gateway.gateway_name,
            description=bank_payment.description
        )
        payment_gateway.ref_num = previous_payment_gateway.ref_num
        payment_gateway.psp_purchase_id = previous_payment_gateway.psp_purchase_id

        if previous_payment_gateway.gateway_name == 'jibit':
            res = jibit_payment_gw_agent.reverse_purchase(
                client_ref_num=payment_gateway.ref_num,
                purchase_id=payment_gateway.psp_purchase_id
            )
            payment_gateway.reverse_status = res['reverse_status']
            payment_gateway.reversed_at = datetime.datetime.now()
            payment_gateway.status = 'SENT'

        else:
            raise SystemError(
                f"you try reverse payment gate way id {previous_payment_gateway_id.id} which its gateway name '{previous_payment_gateway_id} is not defined is system")

        return payment_gateway

    def refund_purchase(
            self,
            previous_payment_gateway_id: int,
            bank_payment_id: int,
            db: Session
    ) -> FncPaymentGateway:
        from ..finance_service import FinanceService
        finance_sr = FinanceService()

        previous_payment_gateway = self.crud.get(db=db, id=previous_payment_gateway_id)
        previous_bank_payment = finance_sr.bank.payment.crud.get(db=db, id=previous_payment_gateway.bank_payment_id)
        bank_payment = finance_sr.bank.payment.crud.get(db=db, id=bank_payment_id)

        if previous_bank_payment.status != 'PAID':
            raise SystemError(f"bank payment id {previous_bank_payment.id} is not PAID, so it is not refundable")

        payment_gateway = finance_sr.bank.gateway.add_item(
            db=db,
            type='refund',
            bank_payment_id=bank_payment_id,
            amount=bank_payment.amount,
            gateway_name=previous_payment_gateway.gateway_name,
            description=bank_payment.description
        )
        payment_gateway.ref_num = previous_payment_gateway.ref_num
        payment_gateway.psp_purchase_id = previous_payment_gateway.psp_purchase_id

        if previous_payment_gateway.gateway_name == 'jibit':
            res = jibit_payment_gw_agent.refund_purchase(
                client_ref_num=payment_gateway.ref_num,
                purchase_id=payment_gateway.psp_purchase_id,
                amount=payment_gateway.amount
            )
            payment_gateway.refund_batch_id = res['batch_id']
            payment_gateway.refund_transfer_id = res['transfer_id']
            payment_gateway.status = 'SENT'

        else:
            raise SystemError(
                f"you try refund payment gate way id {previous_payment_gateway_id} which its gateway name '{previous_payment_gateway_id} is not defined is system")

        return payment_gateway

    def inquiry_psp_status_from_pgp(self, payment_gateway_id: int, db: Session = SessionLocal()):
        pay_gw = self.find_by_id(payment_gateway_id, db)
        res = jibit_payment_gw_agent.inquiry_purchase(purchase_id=pay_gw.psp_purchase_id)

        inquired_pay_gw = res.purchases[0]
        pay_gw.psp_status = inquired_pay_gw.psp_status

        return pay_gw

    def find_by_bank_payment_id(self, bank_payment_id: int, db: Session = SessionLocal()) -> List[FncPaymentGateway]:
        try:
            return self.crud.find_by_bank_payment_id(bank_payment_id, db)

        except Exception as e:
            db.rollback()
            raise e

    def find_last_by_bank_payment_id(self, bank_payment_id: int, db: Session = SessionLocal()) -> FncPaymentGateway:
        try:
            return self.crud.find_last_by_bank_payment_id(bank_payment_id, db)

        except Exception as e:
            db.rollback()
            raise e

    def find_by_id(self, payment_gateway_id: int, db: Session = SessionLocal()) -> FncPaymentGateway:
        res = self.crud.get(db, payment_gateway_id)
        if not res:
            raise PaymentGatewayNotFound

        return res

    def validate_pay_gw_by_ref_num(self, ref_num: str, db: Session = SessionLocal()) -> FncPaymentGateway:
        pay_gw = self.find_item_multi(raise_not_found_exception=False, db=db, ref_num=ref_num)[0]

        if not pay_gw or (datetime.datetime.now() - pay_gw.created_at).seconds > settings.JIBIT_PAY_GW_EXPIRE_TIME:
            raise HTTP_401_Walpay

        return pay_gw

    def test_update(self, id, db: Session = SessionLocal()):
        p = self.find_by_id(id, db=db)
        return self.crud.update(
            db=db,
            db_obj=p,
            obj_in=UpdatePaymentGateway(
                psp_status='something'
            )
        )

    # Admin panel methods
    def get_bank_payments(self, page_number: int, page_size: int, **kwargs):
        data = {'result': [], 'total_count': None}
        result = self.crud.get_all_payment_gateways(db=kwargs['db'], skip=(page_number - 1) * page_size,
                                                    limit=page_size, **CqGetAllPaymentGateways(**kwargs).dict())
        query_result, total_count = result['query_result'], result['total_count']

        data['total_count'] = total_count
        for item in query_result:
            data['result'].append(item._mapping)
        return data


payment_gateway_agent = PaymentGatewayInterface(
    crud=payment_gateway_crud,
    create_schema=CreatePaymentGateway,
    update_schema=UpdatePaymentGateway,
    get_multi_schema=GetMultiFinPaymentGateway
)
