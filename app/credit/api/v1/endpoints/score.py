from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from credit import CreditService
from system.dbs.postgre import get_db
from utils import ResponseManager
from user.interfaces.user import UserInterface
from ..schemas.score import *

router = APIRouter()

score_me_RM = ResponseManager(
    request_model=None,
    response_model=ScoreMeResponse,
    pagination=False,
    is_mock=False
)


@router.get("/me",
            response_model=score_me_RM.response_model(),
            response_description="Get User Credit Score When Logged In"
            )
async def get_user_credit_score(
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["credit:score:me"])
):
    try:
        credit_sr = CreditService()
        score = credit_sr.score.user_credit_score(db=db, user_id=current_user_id)

        score_me_RM.status_code(200)
        return score_me_RM.response({
            'credit_score': score,
            # 'age': age,
        })
    except Exception as e:
        return score_me_RM.exception(e)
