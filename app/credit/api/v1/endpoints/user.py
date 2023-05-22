from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from utils import ResponseManager
from user.interfaces.user import UserInterface
from ..schemas.user import *
router = APIRouter()

info_RM = ResponseManager(
    request_model=None,
    response_model=InfoResponse,
    pagination=False,
    is_mock=False
)


@router.get('/info',
            response_model=info_RM.response_model(),
            response_description="Get User Total Credit"
            )
async def info(
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["credit:info"])
):
    from credit import CreditService
    from utils.jdate_navigator import get_due_date
    credit_service_sr = CreditService()

    try:
        from finance.finance_service import FinanceService
        finance_sr = FinanceService()

        calc_credit_obj = None
        user_credit = credit_service_sr.user.find_item_multi(
            db=db,
            raise_not_found_exception=False,
            user_id=current_user_id
        )

        if not user_credit:
            user_credit = credit_service_sr.user.add_item(db=db, user_id=current_user_id)
        else:
            user_credit = user_credit[0]

        if user_credit.is_locked:
            calc_credit_obj = credit_service_sr.calculator.find_item_multi(db=db, order_by=('id', 'desc'))[0]
        else:
            calc_credit_obj = credit_service_sr.calculator.calculate_credit(
                db=db,
                user_id=current_user_id,
                input_type='credit-info'
            )

        credit_amount = calc_credit_obj.free_credit - calc_credit_obj.used_free_credit + calc_credit_obj.non_free_credit
        max_credit = \
            calc_credit_obj.free_credit \
            + calc_credit_obj.non_free_credit \
            + calc_credit_obj.used_non_free_credit

        total_debt_in_tmn = finance_sr.debt_user.get_total_debt(user_id=current_user_id, db=db)
        credit_dont_need_collateral = calc_credit_obj.free_credit - calc_credit_obj.used_free_credit

        info_RM.status_code(200)
        return info_RM.response(
            {
                'credit': credit_amount,
                'debt': total_debt_in_tmn,
                'max_credit': max_credit,
                'credit_dont_need_collateral': credit_dont_need_collateral,
                'credit_need_collateral': calc_credit_obj.non_free_credit,
                'due_date': get_due_date()

            }
        )
    except Exception as e:
        return info_RM.exception(e)
