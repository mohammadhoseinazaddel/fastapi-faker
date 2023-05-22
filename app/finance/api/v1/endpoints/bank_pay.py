from fastapi import (
    Depends,
    APIRouter)
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from utils import ResponseManager

router = APIRouter()

callback_RM = ResponseManager(
    request_model=None,
    response_model=None,
    pagination=False,
    is_mock=False
)


@router.get('/callback/{pgw_ref_num}',
            response_model=callback_RM.response_model(),
            response_description='Payment Gateway Callback'
            )
def bank_pay_callback(
        pgw_ref_num: str,
        db: Session = Depends(get_db),
):
    try:
        from finance import FinanceService
        finance_sr = FinanceService()

        from order import OrderService

        order_sr = OrderService()

        # get payment gateway and update bank payment
        pgw = finance_sr.bank.payment.find_item_multi(
            db=db,
            ref_num=pgw_ref_num,
        )[0]

        if pgw.status == 'SUCCESS':
            finance_sr.bank.payment.update_item(
                db=db,
                find_by={"id": pgw.bank_payment_id},
                update_to={
                    "status": 'PAID',
                    "success_pgw_id": pgw.id
                }
            )

        elif pgw.status == "FAIL":
            finance_sr.bank.payment.update_item(
                db=db,
                find_by={"id": pgw.bank_payment_id},
                update_to={"status": 'FAILED'}
            )

        # call other services based on bank payment type
        bank_pay = finance_sr.bank.payment.find_item_multi(
            db=db,
            id=pgw.bank_payment_id
        )[0]

        if bank_pay.type == 'pay_order':
            order = order_sr.pay.find_item_multi(
                db=db,
                id=bank_pay.input_unique_id
            )[0]

            return RedirectResponse(url=f'/api/v1/order/pay/callback/{order.identifier}', status_code=301)

    except Exception as e:
        return callback_RM.exception(e)
