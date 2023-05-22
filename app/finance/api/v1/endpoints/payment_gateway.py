from fastapi import (
    Depends,
    APIRouter
)
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from utils import ResponseManager
from ..schemas.payment_gateway import *

router = APIRouter()

send_pay_gw_RM = ResponseManager(
    request_model=SendPayGwCreateRequest,
    response_model=SendPayGwResponse,
    pagination=False,
    is_mock=False
)


@router.get("/send",
            response_model=send_pay_gw_RM.response_model(),
            response_description="Send to Payment Gateway"
            )
def send_to_payment_gateway(
        bank_payment_id: int,
        db: Session = Depends(get_db),
        # current_user_id: str = Security(AuthInterface.get_current_user, scopes=["finance:send_pay_gw"])
):
    try:
        from finance import FinanceService
        finance_sr = FinanceService()

        res = finance_sr.bank.gateway.send_to_payment_gateway(bank_payment_id=bank_payment_id, db=db)
        send_pay_gw_RM.status_code(200)
        return send_pay_gw_RM.response({
            "redirect_url": res["psp_switching_url"]
        })

    except Exception as e:
        return send_pay_gw_RM.exception(e)


pgw_callback_RM = ResponseManager(
    request_model=PgwCallbackRequest,
    response_model=None,
    pagination=False,
    is_mock=False
)


@router.get('/callback/{ref_num}',
            response_model=pgw_callback_RM.response_model(),
            response_description='Payment Gateway Callback'
            )
def pgw_callback(
        ref_num: str,
        info: pgw_callback_RM.request_model(),
        db: Session = Depends(get_db),
):
    try:
        from finance import FinanceService
        finance_sr = FinanceService()

        pgw = finance_sr.bank.gateway.callback(
            ref_num=ref_num,
            amount=info.amount,
            psp_purchase_id=info.psp_purchase_id,
            wage=info.wage,
            payer_ip=info.payer_ip,
            callback_status=info.callback_status,
            psp_ref_num=info.psp_ref_num,
            payer_masked_card_num=info.payer_masked_card_num,
            psp_rrn=info.psp_rrn,
            psp_name=info.psp_name,
            db=db
        )
        redirect = RedirectResponse(
            url=f'/api/v1/finance/bank-pay/callback/{pgw.ref_num}',
            status_code=301
        )
        return redirect

    except Exception as e:
        return pgw_callback_RM.exception(e)
