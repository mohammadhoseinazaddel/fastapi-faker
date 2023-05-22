import datetime

from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from utils import ResponseManager
from user.interfaces.user import UserInterface
from ..schemas.credit_admin import *

router = APIRouter()

user_credit_list_RM = ResponseManager(
    request_model=None,
    response_model=UserCreditResponse,
    pagination=True,
    is_mock=False,
    is_list=True
)


@router.get(
    '/user-all',
    response_description="credit detail",
    response_model=user_credit_list_RM.response_model()
)
async def user_all_credits(
        created_at_ge: datetime.datetime = None,
        created_at_le: datetime.datetime = None,
        page_number: int = Query(default=1, ge=1),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["credit:user:all"]),
        user_id: int = Query(),
        db: Session = Depends(get_db),

):
    from credit import CreditService
    credit_service_sr = CreditService()

    try:

        result = credit_service_sr.calculator.get_user_credit_details(
            db=db,
            user_id=user_id,
            created_at_ge=created_at_ge,
            created_at_le=created_at_le,
            page_number=page_number,
            page_size=10
        )

        user_credit_list_RM.pagination_data(total_count=result['total_count'], current_page=page_number,
                                            page_size=10)
        user_credit_list_RM.status_code(200)
        return user_credit_list_RM.response(result['result'])
    except Exception as e:
        return user_credit_list_RM.exception(e)
