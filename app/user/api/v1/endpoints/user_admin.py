import datetime

from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from user.interfaces.user import UserInterface
from ..managers.user_admin import user_list_RM

router = APIRouter()


@router.get(
    '/all',
    response_description="user detail",
    response_model=user_list_RM.response_model()
)
async def all_users(
        phone_number: str = None,
        user_id: int = None,
        first_name: str = None,
        last_name: str = None,
        verified: bool = None,
        created_at_ge: datetime.datetime = None,
        created_at_le: datetime.datetime = None,
        page_number: int = Query(default=1, ge=1),
        admin_user_id: str = Security(UserInterface.get_current_user, scopes=["users:user:all"]),
        db: Session = Depends(get_db),

):
    from user import UserService
    uer_sr = UserService()

    try:
        result = uer_sr.user.get_user_details(
            db=db,
            phone_number=phone_number,
            created_at_ge=created_at_ge,
            created_at_le=created_at_le,
            page_number=page_number,
            page_size=10,
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            verified=verified
        )

        user_list_RM.pagination_data(total_count=result['total_count'], current_page=page_number, page_size=10)
        user_list_RM.status_code(200)
        return user_list_RM.response(result['result'])
    except Exception as e:
        return user_list_RM.exception(e)
