from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from user.api.v1.managers.merchant import merchant_info_RM, merchant_info_by_login_RM
from user.interfaces.user import UserInterface
from ....interfaces.merchant import merchant_agent

router = APIRouter()


@router.get(
    "/info",
    response_model=merchant_info_RM.response_model(),
    response_description="Get merchants info"
)
def merchants_info(
        db: Session = Depends(get_db),
):
    try:
        response_list = []
        merchants = merchant_agent.find_item_multi(db=db)
        for merchant in merchants:
            response_list.append(
                {
                    'name': merchant.name,
                    'name_fa': merchant.name_fa,
                    'logo_address': merchant.logo_address,
                    'logo_background_color': merchant.logo_background_color
                }
            )
        merchant_info_RM.status_code(200)
        return merchant_info_RM.response(response_list)

    except Exception as e:
        return merchant_info_RM.exception(e)


@router.get(
    "/info-with-login",
    response_model=merchant_info_by_login_RM.response_model(),
    response_description="Get merchants info with login"
)
def merchant_info_by_login(
        current_user_id: int = Security(UserInterface.get_current_user, scopes=["finance:merchant:transfers"]),
        db: Session = Depends(get_db)
):
    try:

        data = UserInterface.get_merchant_info_with_login(
            db=db,
            current_user_id=current_user_id
        )
        merchant_info_by_login_RM.status_code(200)
        return merchant_info_by_login_RM.response(data)

    except Exception as e:
        return merchant_info_by_login_RM.exception(e)
