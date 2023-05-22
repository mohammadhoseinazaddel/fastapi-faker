from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from system.scopes import finance_scopes

from utils import ResponseManager
from user.interfaces.user import UserInterface
from ..schemas.finance_merchant import *
from ..schemas.finance_admin import *

router = APIRouter()

transfer_all_admin_RM = ResponseManager(
    request_model=None,
    response_model=TransfersAdminResponse,
    pagination=True,
    is_mock=False,
    is_list=True
)


@router.get(
    '/transfer',
    response_model=transfer_all_admin_RM.response_model(),
    response_description='transfers'
)
async def merchant_transfers(
        created_at_ge: datetime = None,
        created_at_le: datetime = None,
        transfer_price_ge: float = None,
        transfer_price_le: float = None,
        bank_name: str = None,
        transfer_type: str = None,
        transfer_id: int = None,
        page_number: int = Query(default=1, ge=1),
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["finance:merchant:transfers"])
):
    try:
        from finance import FinanceService
        finance_sr = FinanceService()

        user = UserInterface.find_by_id(user_id=int(current_user_id), db=db)

        result = finance_sr.settle.transfer.get_transfers_list(
            db=db,
            merchant_id=user.merchant.id,
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


transfer_detail_RM = ResponseManager(
    request_model=None,
    response_model=TransferDetailResponse,
    pagination=True,
    is_mock=False
)


@router.get(
    '/transfer/{transfer_id}',
    response_description='transfer detail',
    response_model=transfer_all_admin_RM.response_model()
)
async def merchant_transfer_detail(
        transfer_id: int,
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["finance:merchant:transfer_detail"])
):
    try:
        from finance import FinanceService
        finance_sr = FinanceService()
        transfer_data = finance_sr.transfer.find_item_multi(db=db, id=transfer_id, raise_not_found_exception=True,
                                                            return_first_obj=True)
        data = {
            "id": transfer_data.id,
            "bank_transfer_id": transfer_data.transfer_id,
            "created_at": transfer_data.created_at,
            "account_no": transfer_data.bank_profile.account_no,
            "iban": transfer_data.bank_profile.iban,
            "bank_name": transfer_data.bank_profile.bank_name,
            "amount": transfer_data.amount,
            "type": transfer_data.type,
        }
        transfer_all_admin_RM.status_code(200)
        return transfer_all_admin_RM.response(data)

    except Exception as e:
        return transfer_all_admin_RM.exception(e)


transfer_unsettled_RM = ResponseManager(
    request_model=None,
    response_model=TransferDetailResponse,
    pagination=True,
    is_mock=False,
    is_list=True
)


@router.get(
    '/unsettled',
    response_description='unsettled pwg and credits',
    response_model=transfer_unsettled_RM.response_model()
)
async def merchant_unsettle(
        settlement_type: Literal['ALL', 'all', 'credit', 'pgw'],
        settlement_id: int = None,
        created_at_ge: datetime = None,
        created_at_le: datetime = None,
        transfer_price_ge: float = None,
        transfer_price_le: float = None,
        page_number: int = Query(default=1, ge=1),
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["finance:merchant:transfers"])
):
    try:
        user = UserInterface.find_by_id(user_id=int(current_user_id), db=db)

        from finance import FinanceService
        finance_sr = FinanceService()

        result = finance_sr.settle.get_settle_credit_pwg(
            db=db,
            settlement_id=settlement_id,
            merchant_id=user.merchant.id,
            unsettled=True,
            created_at_ge=created_at_ge,
            created_at_le=created_at_le,
            transfer_price_le=transfer_price_le * 10 if transfer_price_le else None,
            transfer_price_ge=transfer_price_ge * 10 if transfer_price_ge else None,
            page_number=page_number,
            settlement_type=settlement_type,
            page_size=10,
        )
        transfer_unsettled_RM.pagination_data(total_count=result['total_count'], current_page=page_number,
                                              page_size=10)

        transfer_unsettled_RM.status_code(200)
        return transfer_unsettled_RM.response(result['result'])

    except Exception as e:
        return transfer_unsettled_RM.exception(e)


@router.get(
    '/transfer/settles/{transfer_id}',
    response_description='transfer settlement details',
    response_model=transfer_detail_RM.response_model()
)
async def merchant_transfer_settlement_details(
        transfer_id: int,
        created_at_ge: datetime = None,
        created_at_le: datetime = None,
        transfer_price_ge: float = None,
        transfer_price_le: float = None,
        page_number: int = Query(default=1, ge=1),
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["finance:merchant:transfer_detail"])
):
    try:
        user = UserInterface.find_by_id(user_id=int(current_user_id), db=db)
        from finance import FinanceService
        finance_sr = FinanceService()
        result = finance_sr.settle.get_settle_credit_pwg(
            db=db,
            created_at_ge=created_at_ge,
            created_at_le=created_at_le,
            transfer_price_le=transfer_price_le * 10 if transfer_price_le else None,
            transfer_price_ge=transfer_price_ge * 10 if transfer_price_ge else None,
            page_number=page_number,
            page_size=10,
            transfer_id=transfer_id,
            settlement_type="ALL",
            merchant_id=user.merchant.id,
        )
        transfer_detail_RM.pagination_data(total_count=result['total_count'], current_page=page_number,
                                           page_size=10)
        transfer_detail_RM.status_code(200)
        return transfer_detail_RM.response(result['result'])

    except Exception as e:
        return transfer_detail_RM.exception(e)


dashboard_summary_RM = ResponseManager(
    request_model=None,
    response_model=MerchantDashboardSummaryResponse,
    pagination=False,
    is_mock=False
)


@router.get(
    '/dashboard/summary',
    response_description='A summary of merchant orders and settlements.',
    response_model=dashboard_summary_RM.response_model()
)
async def merchant_dashboard_summary(
        current_user_id: int = Security(UserInterface.get_current_user,
                                        scopes=[finance_scopes["merchant:dashboard"]["name"]]),
        db: Session = Depends(get_db)
):
    try:
        from finance import FinanceService
        finance_sr = FinanceService()

        result = finance_sr.merchant_dashboard.summary(current_user_id, db=db)

        dashboard_summary_RM.status_code(200)
        return dashboard_summary_RM.response(result)

    except Exception as e:
        return dashboard_summary_RM.exception(e)


dashboard_plot_RM = ResponseManager(
    request_model=MerchantDashboardRequest,
    response_model=MerchantDashboardPlotResponse,
    pagination=False,
    is_mock=False
)


@router.get(
    '/dashboard/plot',
    response_description='A daily plot of merchant orders and settlements.',
    response_model=dashboard_plot_RM.response_model()
)
async def merchant_dashboard_plot(
        request: dashboard_plot_RM.request_model() = Depends(dashboard_plot_RM.request_model()),
        current_user_id: int = Security(UserInterface.get_current_user,
                                        scopes=[finance_scopes["merchant:dashboard"]["name"]]),
        db: Session = Depends(get_db)
):
    try:
        from finance import FinanceService
        finance_sr = FinanceService()

        result = finance_sr.merchant_dashboard.plot(current_user_id, request.start_time, request.end_time, db=db)

        dashboard_plot_RM.status_code(200)
        return dashboard_plot_RM.response(result)

    except Exception as e:
        return dashboard_plot_RM.exception(e)
