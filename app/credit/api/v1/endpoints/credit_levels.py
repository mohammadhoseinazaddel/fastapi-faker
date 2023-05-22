from fastapi import (
    APIRouter)

from utils import ResponseManager
from ..schemas.credit_levels import *

router = APIRouter()

credit_levels_RM = ResponseManager(
    request_model=None,
    response_model=CreditLevelsResponse,
    pagination=False,
    is_mock=False,
    is_list=True
)


@router.get(
    "",
    response_model=credit_levels_RM.response_model(),
    response_description="Get credit levels"
)
def credit_levels():
    try:
        mock_data = [
            {
                "display_name": "سطح 1",
                "credit": 300000,
                "is_eligble": True
            },
            {
                "display_name": "سطح 2",
                "credit": 500000,
                "is_eligble": False
            },
            {
                "display_name": "سطح 3",
                "credit": 1000000,
                "is_eligble": False
            }
        ]
        credit_levels_RM.status_code(200)
        return credit_levels_RM.response(mock_data)
    except Exception as e:
        return credit_levels_RM.exception(e)
