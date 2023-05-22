import datetime

from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from utils import ResponseManager
from user.interfaces.user import UserInterface
from ..schemas.finance_admin import *

router = APIRouter()

bank_pay_RM = ResponseManager(
    request_model=None,
    response_model=BankPaymentDetailResponse,
    pagination=True,
    is_mock=False,
    is_list=True
)


@router.get(
    '/all',
    response_description="bank payment detail",
    response_model=bank_pay_RM.response_model()
)
async def all_bank_payments(
        phone_number: str = None,
        created_at_ge: datetime = None,
        created_at_le: datetime = None,
        price_ge: float = None,
        price_le: float = None,
        page_number: int = Query(default=1, ge=1),
        admin_user_id: str = Security(UserInterface.get_current_user, scopes=["finance:payment-gateway:all"]),
        db: Session = Depends(get_db),

):
    from finance import FinanceService
    finance_sr = FinanceService()

    try:

        bank_pay_RM.status_code(200)
        result = finance_sr.payment_gateway.get_bank_payments(
            db=db,
            phone_number=phone_number,
            created_at_ge=created_at_ge,
            created_at_le=created_at_le,
            price_le=price_le * 10 if price_le else None,
            price_ge=price_ge * 10 if price_ge else None,
            page_number=page_number,
            page_size=10
        )
        bank_pay_RM.pagination_data(total_count=result['total_count'], current_page=page_number, page_size=10)
        return bank_pay_RM.response(result['result'])

    except Exception as e:
        return bank_pay_RM.exception(e)


transfer_all_admin_RM = ResponseManager(
    request_model=None,
    response_model=TransfersAdminResponse,
    pagination=True,
    is_mock=False,
    is_list=True
)


@router.get(
    '/transfer/all',
    response_description="transfers list",
    response_model=transfer_all_admin_RM.response_model()
)
async def all_transfers(
        created_at_ge: datetime = None,
        created_at_le: datetime = None,
        transfer_price_ge: float = None,
        transfer_price_le: float = None,
        bank_name: str = None,
        transfer_type: str = None,
        transfer_id: int = None,
        page_number: int = Query(default=1, ge=1),
        admin_user_id: str = Security(UserInterface.get_current_user, scopes=["finance:payment-gateway:all"]),
        db: Session = Depends(get_db),

):
    from finance import FinanceService
    finance_sr = FinanceService()

    try:
        result = finance_sr.settle.transfer.get_transfers_list(
            db=db,
            created_at_ge=created_at_ge,
            created_at_le=created_at_le,
            transfer_price_le=transfer_price_le * 10 if transfer_price_le else None,
            transfer_price_ge=transfer_price_ge * 10 if transfer_price_ge else None,
            page_number=page_number,
            bank_name=bank_name,
            transfer_type=transfer_type,
            transfer_id=transfer_id,
            page_size=10
        )
        transfer_all_admin_RM.pagination_data(total_count=result['total_count'], current_page=page_number,
                                              page_size=10)
        transfer_all_admin_RM.status_code(200)
        return transfer_all_admin_RM.response(result['result'])

    except Exception as e:
        return transfer_all_admin_RM.exception(e)
