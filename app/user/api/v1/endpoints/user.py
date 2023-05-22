import jdatetime
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db_without_commit as get_db
from ..managers.user import me_RM, validation_RM
from .... import UserService
from ....exceptions.user import UserInfoNotMatched, UserVerified, NationalCodeIsGiven
from ....interfaces.user import UserInterface

router = APIRouter()


@router.get('/me',
            response_description='User Profile',
            response_model=me_RM.response_model())
async def user_profile(db: Session = Depends(get_db), current_user_id: str = Depends(UserInterface.get_current_user)):
    try:
        from finance import FinanceService
        finance_sr = FinanceService()

        user_sr = UserService()
        user = user_sr.user.find_item_multi(
            db=db,
            id=current_user_id
        )[0]

        bank_profile = finance_sr.bank_profile.find_item_multi(
            db=db,
            user_id=user.id,
            raise_not_found_exception=False,
            return_first_obj=True)

        me_RM.status_code(200)
        return me_RM.response(
            {
                "id": user.id,
                'mobile': user.mobile,
                'national_code': user.national_code,
                'birth_date': user.birth_date,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_image': user.profile_image,
                'last_login': user.last_login,
                'iban_number': bank_profile.iban if bank_profile else None
            }
            )

    except Exception as e:
        return me_RM.exception(e)


@router.get('/test-token')
async def test_token(db: Session = Depends(get_db), current_user_id: str = Depends(UserInterface.get_current_user)):
    return current_user_id


@router.post('/identity-validation',
             response_model=validation_RM.response_model(),
             response_description='User Identity Validation'
             )
async def identity_validation(
        user_info: validation_RM.request_model(),
        db: Session = Depends(get_db),
        current_session_id: str = Security(UserInterface.get_current_session, scopes=["user:validation"])
):
    try:
        user_sr = UserService()

        session = user_sr.user.session.find_item_multi(
            db=db,
            id=current_session_id
        )[0]

        user = user_sr.user.find_item_multi(
            db=db,
            id=session.user_id
        )[0]

        if user.verified:
            raise UserVerified

        if user.national_code != user_info.national_code:
            national_code_users = user_sr.user.find_item_multi(
                db=db,
                national_code=user_info.national_code,
                raise_not_found_exception=False
            )
            if national_code_users:
                raise NationalCodeIsGiven

        user_sr.user.update_item(
            db=db,
            find_by={"id": session.user_id},
            update_to={
                "birth_date": user_info.birth_date,
                "national_code": user_info.national_code
            }
        )
        db.commit()

        user_sr.user.identity_validate(
            user_id=user.id,
            db=db
        )

        if user.verified:
            kyc_rec = user_sr.user.kyc.find_item_multi(
                db=db,
                id=user.kyc_id
            )[0]

            validation_RM.status_code(200)
            access_token = user_sr.user.get_access_token(given_id=user.id, db=db)
            refresh_token = user_sr.user.get_refresh_token(given_id=user.id, db=db)

            user_sr.user.session.update_item(
                db=db,
                find_by={"id": current_session_id},
                update_to={"is_valid": False}
            )
            db.commit()
            return validation_RM.response({
                "new_access_token": access_token,
                "new_refresh_token": refresh_token,
                "token_type": "bearer",
                "user": {
                    "national_code": user.national_code if user.national_code else None,
                    "birth_date": jdatetime.date.fromgregorian(date=user.birth_date) if user.birth_date else None,
                    "birth_date_georgian": user.birth_date,
                    "sabte_ahval_verified": kyc_rec.sabte_ahval_verified,
                    "shahkar_verified": kyc_rec.shahkar_verified,
                    "verified": user.verified
                }})
        else:
            raise UserInfoNotMatched

    except Exception as e:
        return validation_RM.exception(e)
