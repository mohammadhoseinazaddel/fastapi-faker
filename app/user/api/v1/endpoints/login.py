from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from ext_services.wallex.exceptions.oauth import WallexStateNotFound
from ext_services.wallex.interfaces.login import wallex_login_agent
from ext_services.wallex.models.schemas.user_login import GetMultiUsrWlxState
from system.config import settings
from system.dbs.postgre import get_db
from user.api.v1.managers.login import wallex_login_RM, refresh_token_RM
from user.exceptions.auth import InvalidCredential
from .... import UserService

router = APIRouter()


@router.post("")
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user_sr = UserService()
        user = user_sr.user.authenticate_user(username=form_data.username, password=form_data.password, db=db)
        access_token = user_sr.user.get_access_token(given_id=user.id, db=db)
        refresh_token = user_sr.user.get_refresh_token(given_id=user.id, db=db)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    except InvalidCredential:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@router.post("/token", description='Refresh Tokens', response_model=refresh_token_RM.response_model())
async def refresh_token(form_data: refresh_token_RM.request_model(), db: Session = Depends(get_db)):
    try:
        user_sr = UserService()
        refresh_token_RM.status_code(200)
        return refresh_token_RM.response(
            user_sr.user.renew_tokens(
                access_token=form_data.access_token,
                refresh_token=form_data.refresh_token,
                db=db
            )
        )

    except Exception as e:
        return refresh_token_RM.exception(e)


@router.get('/wallex-callback', description='Call Back Wallex Login')
async def wallex_login_callback(code: str, state: str, db: Session = Depends(get_db)):
    try:
        wallex_login_record = wallex_login_agent.crud.get_multi(db=db, filter_obj=GetMultiUsrWlxState(state=state))
        if not wallex_login_record:
            raise WallexStateNotFound
        else:
            wallex_login_record = wallex_login_record[0]

        wallex_login_agent.update_item(db=db, find_by={'state': wallex_login_record.state}, update_to={'code': code})

        token = wallex_login_agent.get_wallex_token_by_code(db=db, code=code, state=wallex_login_record.state)

        wallex_user_info = wallex_login_agent.get_wallex_user(db=db, access_token=token)

        #  handle NationalCodeIsGiven Error
        temp_user = user_agent.find_by_mobile(db=db, mobile=wallex_user_info.mobile, raise_not_found_exception=False)
        if not temp_user and user_agent.find_by_national_code(
                db=db,
                national_code=wallex_user_info.national_code,
                raise_not_found_exception=False
        ):
            wallex_login_agent.update_item(db=db, find_by={'state': state},
                                           update_to={'wallpay_error': 'NationalCodeIsGiven'})

        else:
            wallpay_user = user_agent.create_or_update_based_on_wallex_user_info(
                db=db,
                wallex_kyc_level=wallex_user_info.kyc_level,
                mobile=wallex_user_info.mobile,
                national_code=wallex_user_info.national_code,
                first_name=wallex_user_info.first_name,
                last_name=wallex_user_info.last_name,
                birth_date=wallex_user_info.birth_date
            )
            wallex_login_agent.update_item(db=db, find_by={'state': state}, update_to={'user_id': wallpay_user.id})

        redirect_url = settings.FRONT_BASE_URL + '/oauth/callback'
        query_str = f'?state={wallex_login_record.state}'
        query_str += f'&order_uuid={wallex_login_record.order_uuid}' if wallex_login_record.order_uuid else ''
        return RedirectResponse(url=redirect_url + query_str, status_code=307)

    except WallexStateNotFound:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='در حال حاضر ارتباط با والکس مقدور نمی باشد، لطفا مجددا تلاش نمایید',
        )


@router.get("/wallex", description='Login By Wallex', response_model=wallex_login_RM.response_model())
async def wallex_login(order_uuid: str = None, db: Session = Depends(get_db)):
    try:
        wallex_login_record = wallex_login_agent.create_wallex_login_request(order_uuid=order_uuid, db=db)
        wallex_login_RM.status_code(200)
        return wallex_login_RM.response(
            {
                'redirect_url': wallex_login_record.wallex_login_url
            }
        )

    except Exception as e:
        print(e)
        return wallex_login_RM.exception(e)

# @router.get('/by-state', description='get token by state', response_model=login_by_state_RM.response_model())
# async def login_by_state(
#         state: str,
#         db: Session = Depends(get_db)
# ):
#     try:
#         from user import UserService
#         user_sr = UserService()
#
#         wallex_login_record = wallex_login_agent.find_by_state_for_login(state=state, db=db)
#         if not wallex_login_record.user_id:
#             if wallex_login_record.wallpay_error:
#                 raise NationalCodeIsGiven
#
#             else:
#                 raise UserNotFound
#
#         user = user_sr.user.find_item_multi(db=db, id=wallex_login_record.user_id)[0]
#         user.user_logged_in(db=db)
#         db.add(user)
#         db.commit()
#         db.refresh(user)
#
#         login_by_state_RM.status_code(200)
#         return login_by_state_RM.response(
#             {
#                 "access_token": user_agent.get_token(db, user.id),
#                 "token_type": "bearer",
#                 "user": {
#                     "national_code": user.national_code if user.national_code else None,
#                     "birth_date": user.convert_birthdate_to_persian(),
#                     "birth_date_georgian": user.birth_date,
#                     "sabte_ahval_verified": user.sabte_ahval_verified,
#                     "shahkar_verified": user.shahkar_verified,
#                     "verified": user.is_verified()
#                 }
#             }
#         )
#
#     except Exception as e:
#         return login_by_state_RM.exception(e)
