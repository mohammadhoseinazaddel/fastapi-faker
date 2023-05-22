from fastapi.responses import RedirectResponse
from fastapi import (
    Request,
    Depends,
    Security,
    HTTPException,
    APIRouter
)
from sqlalchemy.orm import Session
from system.dbs.postgre import get_db

router = APIRouter()


# DO NOT CHANGE THIS END POINT URL ESPECIALLY 'jibit_pay_gw_callback' PART
@router.post("/{client_ref_num}/jibit_pay_gw_callback",
             response_description="Jibit Payment Gateway Callback"
             )
async def jibit_pay_gw_callback(
        req: Request,
        client_ref_num: str,
        db: Session = Depends(get_db),
):
    try:
        if req.headers['Content-Type'] == 'application/x-www-form-urlencoded':
            items = {}

            path_params = req.path_params
            if 'client_ref_num' in path_params:
                items['client_ref_num'] = path_params['client_ref_num']

            body = await req.body()
            body = body.decode('ascii')
            for i in body.split('&'):
                d = i.split('=')
                items[d[0]] = d[1]

            body = {
                'info': {
                    "ref_num": items['client_ref_num'],
                    "amount": int(items['amount']),
                    "psp_purchase_id": items['purchaseId'],
                    "wage": items['wage'],
                    "payer_ip": items['payerIp'],
                    "callback_status": items['status'],
                    "psp_ref_num": items['pspReferenceNumber'] if "pspReferenceNumber" in items.keys() else None,
                    "payer_masked_card_num": items['payerMaskedCardNumber'],
                    "psp_rrn": items['pspRRN'] if "pspRRN" in items.keys() else None,
                    "psp_name": items['pspName'] if "pspName" in items.keys() else None,
                },
                "db": db
            }

            redirect = RedirectResponse(
                url=f'/api/v1/finance/payment-gateway/callback/{items["client_ref_num"]}',
                status_code=301
            )
            redirect.body = body

            # response_url = payment_gateway_agent.callback(
            #     ref_num=items['client_ref_num'],
            #     amount=int(items['amount']),
            #     psp_purchase_id=items['purchaseId'],
            #     wage=items['wage'],
            #     payer_ip=items['payerIp'],
            #     callback_status=items['status'],
            #     psp_ref_num=items['pspReferenceNumber'] if "pspReferenceNumber" in items.keys() else None,
            #     payer_masked_card_num=items['payerMaskedCardNumber'],
            #     psp_rrn=items['pspRRN'] if "pspRRN" in items.keys() else None,
            #     psp_name=items['pspName'] if "pspName" in items.keys() else None,
            #     db=db
            # )
            #
            # return RedirectResponse(response_url, status_code=301)

            return redirect

        else:
            print(req.headers['Content-Type'])
            # logger something
            # return RedirectResponse(res['redirect_url'])

    except Exception as e:
        raise e
