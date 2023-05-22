from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from utils import ResponseManager
from user.interfaces.user import UserInterface
from ..schemas.bank_profile import *

router = APIRouter()

create_bank_profile_RM = ResponseManager(
    request_model=CreateBankProfileRequest,
    response_model=CreateBankProfileResponse,
    pagination=False,
    is_mock=False
)


@router.post('/create-user-bank-profile',
             response_model=create_bank_profile_RM.response_model(),
             response_description='Create user bank profile'
             )
async def create_user_bank_profile(
        user_info: create_bank_profile_RM.request_model(),
        db: Session = Depends(get_db),
        current_user_id: str = Security(
            UserInterface.get_current_user,
            scopes=["finance:bank-profile:create-user-bank-profile"]
        )
):
    try:
        from finance import FinanceService
        finance_sr = FinanceService()

        create_bank_profile_RM.status_code(201)
        response = finance_sr.bank_profile.create_user_bank_profile(
            db=db,
            user_id=current_user_id,
            card_number=user_info.card_number,
        )

        return create_bank_profile_RM.response(response)

    except Exception as e:
        return create_bank_profile_RM.exception(e)
