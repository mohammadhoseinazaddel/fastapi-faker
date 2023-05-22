from fastapi import (
    Depends,
    APIRouter)
from sqlalchemy.orm import Session
from system.dbs.postgre import get_db
from ext_services.jibit.payment_gateway.inquiry_purchase import jibit_pay_gw_inquiry_purchase

router = APIRouter()


@router.get("/inquiry",
            response_description="Jibit Payment Gateway Inquiry"
            )
def jibit_payment_gateway_inquiry(
        client_ref_num: str = None,
        from_date=None,
        to_date=None,
        page: int = 0,
        psp_ref_num: str = None,
        psp_rrn: str = None,
        psp_trace_num: str = None,
        purchase_id: str = None,
        size: int = 0,
        pgp_status: str = None,
        user_identifier: str = None,
        db: Session = Depends(get_db),
):
    try:
        return jibit_pay_gw_inquiry_purchase(
            client_ref_num=client_ref_num,
            from_date=from_date,
            to_date=to_date,
            page=page,
            psp_ref_num=psp_ref_num,
            psp_rrn=psp_rrn,
            psp_trace_num=psp_trace_num,
            purchase_id=purchase_id,
            size=size,
            pgp_status=pgp_status,
            user_identifier=user_identifier,
        )

    except Exception as e:
        raise e
