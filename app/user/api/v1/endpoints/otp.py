import jdatetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from system.config import settings
from system.dbs.postgre import get_db_without_commit as get_db
from utils.response_manager import ResponseManager
from ..schemas.otp import *

router = APIRouter()

send_otp_RM = ResponseManager(
    request_model=SendOtpRequest,
    response_model=SendOtpResponse,
    pagination=False,
    is_mock=False,
    is_list=False
)


@router.post("/send",
             response_model=send_otp_RM.response_model(),
             response_description="Sign up / Login", )
async def send_otp(send: send_otp_RM.request_model() = Depends(send_otp_RM.request_model()),
                   db: Session = Depends(get_db), ):
    try:
        from user import UserService
        user_sr = UserService()

        res = user_sr.otp.send_otp(
            mobile=send.mobile,
            db=db
        )

        send_otp_RM.status_code(200)
        return send_otp_RM.response({
            "mobile": send.mobile,
            "send_sms_status": res,
            "message": f"شما می توانید پس از {settings.OTP_TIME_OUT} ثانیه مجددا درخواست رمز نمایید"
        })

    except Exception as e:
        return send_otp_RM.exception(e)


check_otp_RM = ResponseManager(
    request_model=CheckOtpRequest,
    response_model=CheckOtpResponse,
    pagination=False,
    is_mock=False
)


@router.post("/check",
             response_model=check_otp_RM.response_model(),
             response_description="Check OTP", )
async def check_otp(otp_check: check_otp_RM.request_model(), db: Session = Depends(get_db)):
    try:
        from user import UserService
        user_sr = UserService()

        user_sr.otp.check_otp(
            db=db,
            mobile=otp_check.mobile,
            otp=otp_check.otp
        )

        user = user_sr.user.find_item_multi(
            db=db,
            mobile=otp_check.mobile,
            raise_not_found_exception=False
        )
        if user:
            user = user[0]

        else:
            user = user_sr.user.add_item(
                db=db,
                mobile=otp_check.mobile
            )

        rudimentary_group = user_sr.group.find_item_multi(
            db=db,
            name='rudimentary'
        )[0]
        user_sr.user.add_to_group(
            user_id=user.id,
            group_id=rudimentary_group.id,
            db=db
        )
        user_sr.user.set_login_time(user_id=user.id, db=db)

        access_token = user_sr.user.get_access_token(given_id=user.id, db=db)
        refresh_token = user_sr.user.get_refresh_token(given_id=user.id, db=db)

        db.commit()
        db.refresh(user)

        check_otp_RM.status_code(200)

        return check_otp_RM.response({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "national_code": user.national_code if user.national_code else None,
                "birth_date": jdatetime.date.fromgregorian(date=user.birth_date) if user.birth_date else None,
                "birth_date_georgian": user.birth_date,
                # "sabte_ahval_verified": user.sabte_ahval_verified,
                # "shahkar_verified": user.shahkar_verified,
                "verified": user.verified
            }})

    except Exception as e:
        return check_otp_RM.exception(e)
