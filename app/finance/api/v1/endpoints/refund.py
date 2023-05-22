import traceback

from fastapi import Depends, APIRouter, Security
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from utils import ResponseManager
from user.interfaces.user import UserInterface
from ..schemas.refund import *

router = APIRouter()

refund_RM = ResponseManager(
    request_model=RefundRequest,
    response_model=RefundResponse,
    pagination=False,
    is_mock=False
)


@router.post(
    '/refund',
    response_model=refund_RM.response_model(),
    response_description='just for user'
)
async def refund(
        request_model: refund_RM.request_model(),
        db: Session = Depends(get_db),
        current_user_and_merchant: list = Security(
            UserInterface.get_current_user_and_merchant,
            scopes=["finance:refund:refund"]
        )
):
    try:
        from finance import FinanceService
        finance_sr = FinanceService()

        result = finance_sr.refund.refund(
            db=db,
            order_uuid=request_model.order_uuid,
            merchant_id=current_user_and_merchant[1],
            merchant_user_id=current_user_and_merchant[0],
            refund_amount=request_model.amount
        )

        refund_RM.status_code(200)
        return refund_RM.response(result)

    except Exception as e:
        traceback.print_exc()
        db.rollback()
        return refund_RM.exception(e)


refund_detail_RM = ResponseManager(
    request_model=RefundDetailRequest,
    response_model=RefundDetailResponse,
    pagination=False,
    is_mock=False
)


@router.get(
    '/refund-detail',
    response_model=refund_detail_RM.response_model(),
    response_description='detail of refund'
)
async def refund_detail(
        order_uuid: str,
        db: Session = Depends(get_db),
        current_user: list = Security(
            UserInterface.get_current_user,
            scopes=["finance:refund:refund-detail"]
        )
):
    try:
        from finance import FinanceService
        finance_sr = FinanceService()

        result = finance_sr.refund.get_refund_detail(
            db=db,
            order_uuid=order_uuid,
            user_id=current_user
        )

        refund_detail_RM.status_code(200)
        return refund_detail_RM.response(result)

    except Exception as e:
        traceback.print_exc()
        db.rollback()
        return refund_RM.exception(e)


submit_refund_after_add_bank_profile_RM = ResponseManager(
    request_model=SubmitRefundAfterAddBankProfileRequest,
    response_model=SubmitRefundAfterAddBankProfileResponse,
    pagination=False,
    is_mock=False
)


@router.post(
    '/submit-refund-after-add-bank-profile',
    response_model=submit_refund_after_add_bank_profile_RM.response_model(),
    response_description='after user add bank profile this api is ready to use'
)
async def submit_refund_after_add_bank_profile(
        request_model: submit_refund_after_add_bank_profile_RM.request_model(),
        db: Session = Depends(get_db),
        current_user: list = Security(
            UserInterface.get_current_user,
            scopes=["finance:refund:submit-refund-after-add-bank-profile"]
        )
):
    try:
        from finance import FinanceService
        finance_sr = FinanceService()

        result = finance_sr.refund.submit_refund_after_user_create_bank_profile(
            db=db,
            order_uuid=request_model.order_uuid,
            user_id=current_user
        )

        submit_refund_after_add_bank_profile_RM.status_code(201)
        return submit_refund_after_add_bank_profile_RM.response(result)

    except Exception as e:
        traceback.print_exc()
        db.rollback()
        return refund_RM.exception(e)
