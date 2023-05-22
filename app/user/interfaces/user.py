import datetime

import pytz
from fastapi import HTTPException, status, Depends
from fastapi.security import SecurityScopes
from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.config import settings
from system.dbs.postgre import SessionLocal
from .auth import jwt_agent, oauth2_scheme, JwtInterface
from .group import group_agent
from .kyc import kyc_agent
from .session import session_agent
from ..api.v1.schemas.user_admin import CqGetUserDetails
from ..exceptions import user as user_exception
from ..exceptions.merchant import MerchantBankProfileNotFound
from ..exceptions.user import UserVerified, ShahkarServiceError, IdentityServiceError
from ..models.schemas.kyc import KycCreateSchema
from ..models.schemas.user import UserCreateSchema, UserUpdateSchema, UserGetMultiSchema
from ..models.schemas.user_groups import UserGroupsCreateSchema, UserGroupsUpdateSchema, UserGroupsGetMultiSchema
from ..models.schemas.user_merchants import UserMerchantsCreateSchema, UserMerchantsUpdateSchema, \
    UserMerchantsGetMultiSchema
from ..models.user import user_crud, UsrUser
from ..models.user_groups import user_groups_crud, UsrUserGroups
from ..models.user_merchants import user_merchants_crud, UsrUserMerchants


class UserGroupsInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)

        self.crud = user_groups_crud
        self.model = UsrUserGroups


user_groups_agent = UserGroupsInterface(
    crud=user_groups_crud,
    create_schema=UserGroupsCreateSchema,
    update_schema=UserGroupsUpdateSchema,
    get_multi_schema=UserGroupsGetMultiSchema
)


class UserMerchantsInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)

        self.crud = user_merchants_crud
        self.model = UsrUserMerchants


user_merchants_agent = UserMerchantsInterface(
    crud=user_merchants_crud,
    create_schema=UserMerchantsCreateSchema,
    update_schema=UserMerchantsUpdateSchema,
    get_multi_schema=UserMerchantsGetMultiSchema
)


class UserInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema, exception):
        super().__init__(crud, create_schema, update_schema, get_multi_schema, exception)

        self.exceptions = exception
        self.crud = crud
        self.model = UsrUser
        self.user_groups = user_groups_agent
        self.user_merchants = user_merchants_agent
        self.kyc = kyc_agent
        self.session = session_agent
        self.jwt = jwt_agent

    def set_login_time(self, user_id: int, db: Session = SessionLocal()):
        user = self.find_item_multi(
            db=db,
            id=user_id
        )[0]
        user.last_login = datetime.datetime.now()

    def authenticate_user(self, username: str, password: str, db: Session = SessionLocal()):
        user = self.find_item_multi(
            db=db,
            username=username,
            raise_not_found_exception=False
        )

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if not self.jwt.verify_password(password, user[0].hashed_pass):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return user[0]

    @staticmethod
    def get_current_user_and_merchant(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
        try:
            # Token Validations
            token_data = JwtInterface.decrypt_token(
                token=token,
                secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
                algorithm=settings.ACCESS_TOKEN_ALGORITHM
            )

            # Token Validations: check time
            if token_data.expire_at < datetime.datetime.now().replace(tzinfo=pytz.UTC):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            # Token Validations: check scopes
            for scope in security_scopes.scopes:
                if scope not in token_data.scopes:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            # Session
            db = SessionLocal()
            session = session_agent.find_item_multi(
                db=SessionLocal(),
                token=token
            )
            if not session:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            else:
                session = session[0]

            if not session.is_valid:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            #  ANY CRITERIA FOR SESSION CHECK COULD HANDLE IN THIS LINE

            session_agent.update_item(
                db=db,
                find_by={"id": session.id},
                update_to={"token_last_used_at": datetime.datetime.now()}
            )
            db.commit()

            # get user
            db = SessionLocal()
            user = db.query(UsrUser).filter(UsrUser.id == int(token_data.id)).first()

            if not user.merchant.id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            return [user.id, user.merchant.id]

        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    def get_access_token(self, given_id: int, db: Session = SessionLocal()) -> str:
        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = self.jwt.generate_token(
            given_id=given_id,
            scopes=self.get_user_scopes_name_list(user_id=given_id, db=db),
            expire_at=expire_at,
            secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
            algorithm=settings.ACCESS_TOKEN_ALGORITHM
        )

        self.session.add_item(
            db=db,
            token=token,
            user_id=given_id,
            expire_at=expire_at,
            token_last_used_at=datetime.datetime.now(),
            token_first_used_at=datetime.datetime.now()
        )

        return token

    def get_refresh_token(self, given_id: int, db: Session = SessionLocal()) -> str:
        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        token = self.jwt.generate_token(
            given_id=given_id,
            scopes=self.get_user_scopes_name_list(user_id=given_id, db=db),
            expire_at=expire_at,
            secret_key=settings.REFRESH_TOKEN_SECRET_KEY,
            algorithm=settings.REFRESH_TOKEN_ALGORITHM
        )

        self.session.add_item(
            db=db,
            token=token,
            user_id=given_id,
            expire_at=expire_at,
            token_last_used_at=datetime.datetime.now(),
            token_first_used_at=datetime.datetime.now()
        )

        return token

    def renew_tokens(
            self,
            access_token: str,
            refresh_token: str,
            db: Session = SessionLocal()
    ):
        refresh_token_data = self.jwt.decrypt_token(
            token=refresh_token,
            secret_key=settings.REFRESH_TOKEN_SECRET_KEY,
            algorithm=settings.REFRESH_TOKEN_ALGORITHM
        )
        utc = pytz.UTC
        if refresh_token_data.expire_at + datetime.timedelta(
                hours=settings.MINIMUM_TIME_FOR_RENEW_REFRESH_TOKEN) > datetime.datetime.now().replace(tzinfo=utc):

            session_refresh = self.session.find_item_multi(
                db=db,
                token=refresh_token,
                raise_not_found_exception=False
            )
            if session_refresh:
                session_refresh = session_refresh[0]

                self.session.update_item(
                    db=db,
                    find_by={"id": session_refresh.id},
                    update_to={"is_valid": False}
                )

            refresh_token = self.get_refresh_token(
                given_id=refresh_token_data.id,
                db=db
            )

        session_access = self.session.find_item_multi(
            db=db,
            token=access_token,
            raise_not_found_exception=False
        )
        if session_access:
            session_access = session_access[0]
            self.session.update_item(
                db=db,
                find_by={"id": session_access.id},
                update_to={"is_valid": False}
            )

        access_token = self.get_access_token(
            given_id=refresh_token_data.id,
            db=db
        )

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    @staticmethod
    def find_by_id(user_id: int, db: Session):
        return user_crud.get_all_user_details(db=db, user_id=user_id, ).first()

    @staticmethod
    def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
        try:
            token_data = JwtInterface.decrypt_token(
                token=token,
                secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
                algorithm=settings.ACCESS_TOKEN_ALGORITHM
            )

            # check time
            if token_data.expire_at < datetime.datetime.now().replace(tzinfo=pytz.UTC):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            # check scopes
            for scope in security_scopes.scopes:
                if scope not in token_data.scopes:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            # session
            db = SessionLocal()
            session = session_agent.find_item_multi(
                db=SessionLocal(),
                token=token
            )
            if not session:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            else:
                session = session[0]

            if not session.is_valid:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            #  ANY CRITERIA FOR SESSION CHECK COULD HANDLE IN THIS LINE

            session_agent.update_item(
                db=db,
                find_by={"id": session.id},
                update_to={"token_last_used_at": datetime.datetime.now()}
            )
            db.commit()

            return token_data.id

        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def get_current_user_and_merchant(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
        try:
            # Token Validations
            token_data = JwtInterface.decrypt_token(
                token=token,
                secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
                algorithm=settings.ACCESS_TOKEN_ALGORITHM
            )

            # Token Validations: check time
            if token_data.expire_at < datetime.datetime.now().replace(tzinfo=pytz.UTC):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            # Token Validations: check scopes
            for scope in security_scopes.scopes:
                if scope not in token_data.scopes:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            # Session
            db = SessionLocal()
            session = session_agent.find_item_multi(
                db=SessionLocal(),
                token=token
            )
            if not session:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            else:
                session = session[0]

            if not session.is_valid:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            #  ANY CRITERIA FOR SESSION CHECK COULD HANDLE IN THIS LINE

            session_agent.update_item(
                db=db,
                find_by={"id": session.id},
                update_to={"token_last_used_at": datetime.datetime.now()}
            )
            db.commit()

            # get user
            db = SessionLocal()
            user = db.query(UsrUser).filter(UsrUser.id == int(token_data.id)).first()

            if not user.merchant.id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            return [user.id, user.merchant.id]

        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def get_current_session(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
        try:
            token_data = JwtInterface.decrypt_token(
                token=token,
                secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
                algorithm=settings.ACCESS_TOKEN_ALGORITHM
            )

            # check time
            if token_data.expire_at < datetime.datetime.now().replace(tzinfo=pytz.UTC):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            # check scopes
            for scope in security_scopes.scopes:
                if scope not in token_data.scopes:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            # session
            db = SessionLocal()
            session = session_agent.find_item_multi(
                db=SessionLocal(),
                token=token
            )
            if not session:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            else:
                session = session[0]

            if not session.is_valid:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            #  ANY CRITERIA FOR SESSION CHECK COULD HANDLE IN THIS LINE

            session_agent.update_item(
                db=db,
                find_by={"id": session.id},
                update_to={"token_last_used_at": datetime.datetime.now()}
            )
            db.commit()

            return session.id

        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    def identity_validate(
            self,
            user_id: int,
            db: Session = SessionLocal()
    ):
        user = self.find_item_multi(
            db=db,
            id=user_id
        )[0]

        if user.verified:
            raise UserVerified

        kyc_draft = KycCreateSchema(
            sabte_ahval_inquired_at=datetime.datetime.now(),
            shahkar_inquired_at=datetime.datetime.now(),
        )

        # استعلام ثبت احوال
        identity_service_error = False
        res = self.kyc.get_identity(user.national_code, user.birth_date)

        if not res['is_valid'] and not res['had_system_error']:
            kyc_draft.sabte_ahval_verified = False
            kyc_draft.sabte_ahval_inquired_at = datetime.datetime.now()

        if res['had_system_error']:
            kyc_draft.sabte_ahval_verified = False
            kyc_draft.sabte_ahval_inquired_at = datetime.datetime.now()
            identity_service_error = True

        if res['is_valid']:
            if not res['user_info']['is_alive']:
                kyc_draft.sabte_ahval_verified = False
                kyc_draft.sabte_ahval_inquired_at = datetime.datetime.now()

            else:
                kyc_draft.sabte_ahval_verified = True
                kyc_draft.sabte_ahval_inquired_at = datetime.datetime.now()

                kyc_draft.first_name = res['user_info']['first_name']
                kyc_draft.last_name = res['user_info']['last_name']
                kyc_draft.father_name = res['user_info']['father_name']
                kyc_draft.first_name = res['user_info']['first_name']
                kyc_draft.sabte_ahval_track_no = res['user_info']['provider_tracker_id']

        # استعلام شاهکار
        shahkar_service_error = False
        res = self.kyc.shahkar_validation(user.national_code, user.mobile)
        if not res['had_system_error']:
            if not res['is_valid']:
                kyc_draft.shahkar_verified = False
                kyc_draft.shahkar_inquired_at = datetime.datetime.now()
            else:
                kyc_draft.shahkar_verified = True
                kyc_draft.shahkar_inquired_at = datetime.datetime.now()

        if res['had_system_error']:
            kyc_draft.shahkar_verified = False
            kyc_draft.shahkar_inquired_at = datetime.datetime.now()
            shahkar_service_error = True

        # update user and kyc record based on inquiry results
        if user.kyc_id:
            self.kyc.update_item(
                db=db,
                find_by={"id": user.kyc_id},
                update_to={
                    "sabte_ahval_inquired_at": kyc_draft.sabte_ahval_inquired_at,
                    "sabte_ahval_track_no": kyc_draft.sabte_ahval_track_no,
                    "sabte_ahval_verified": kyc_draft.sabte_ahval_verified,
                    "shahkar_inquired_at": kyc_draft.shahkar_inquired_at,
                    "shahkar_verified": kyc_draft.shahkar_verified,
                    "first_name": kyc_draft.first_name,
                    "last_name": kyc_draft.last_name,
                    "father_name": kyc_draft.father_name
                }
            )

        else:
            kyc_record = self.kyc.add_item(
                db=db,
                sabte_ahval_inquired_at=kyc_draft.sabte_ahval_inquired_at,
                sabte_ahval_track_no=kyc_draft.sabte_ahval_track_no,
                sabte_ahval_verified=kyc_draft.sabte_ahval_verified,
                shahkar_inquired_at=kyc_draft.shahkar_inquired_at,
                shahkar_verified=kyc_draft.shahkar_verified,
                first_name=kyc_draft.first_name,
                last_name=kyc_draft.last_name,
                father_name=kyc_draft.father_name
            )

            self.update_item(
                db=db,
                find_by={"id": user.id},
                update_to={"kyc_id": kyc_record.id}
            )

        if identity_service_error:
            raise IdentityServiceError

        if shahkar_service_error:
            raise ShahkarServiceError

        # verified user
        kyc_record = self.kyc.find_item_multi(
            db=db,
            id=user.kyc_id
        )[0]

        if kyc_record.sabte_ahval_verified and kyc_record.shahkar_verified:
            self.update_item(
                db=db,
                find_by={"id": user.id},
                update_to={
                    "verified": True,
                    "verified_by": "Wallpay_inquiry",
                    "verified_at": datetime.datetime.now().replace(tzinfo=pytz.UTC)
                }
            )
            # add to mobile group
            mobile_group = group_agent.find_item_multi(
                db=db,
                name='mobile'
            )[0]
            self.add_to_group(
                db=db,
                user_id=user_id,
                group_id=mobile_group.id,
            )
            db.commit()

            from user_assets.service_agent import UserAssetsService
            from credit import CreditService
            user_asset_SR = UserAssetsService()
            credit_sr = CreditService()
            # user_asset_SR.fiat_wallets.create_user_fiat_wallet(user_id=self.id, db=db)
            credit_sr.user.add_item(db=db, user_id=user.id)

    def add_to_group(
            self,
            user_id: int,
            group_id: int,
            db: Session = SessionLocal()
    ):
        exist = self.user_groups.find_item_multi(
            db=db,
            user_id=user_id,
            group_id=group_id,
            raise_not_found_exception=False
        )

        if exist:
            return True

        self.user_groups.add_item(
            db=db,
            user_id=user_id,
            group_id=group_id
        )

        return True

    def add_to_merchant(
            self,
            user_id: int,
            merchant_id: int,
            db: Session = SessionLocal()
    ):
        exist = self.user_merchants.find_item_multi(
            db=db,
            user_id=user_id,
            merchant_id=merchant_id,
            raise_not_found_exception=False
        )

        if exist:
            return True

        self.user_merchants.add_item(
            db=db,
            user_id=user_id,
            merchant_id=merchant_id
        )

        return True

    def delete_from_a_group(
            self,
            user_id: int,
            group_id: int,
            db: Session = SessionLocal()
    ):
        exist = self.user_groups.find_item_multi(
            db=db,
            user_id=user_id,
            group_id=group_id,
            raise_not_found_exception=False
        )

        if not exist:
            return True

        res = self.user_groups.delete_item(
            db=db,
            find_by={
                "user_id": user_id,
                "group_id": group_id
            }
        )
        return True if res else False

    def get_user_scopes_name_list(
            self,
            user_id: int,
            db: Session = SessionLocal()
    ):
        user_groups = self.user_groups.find_item_multi(
            db=db,
            user_id=user_id,
        )

        groups_ids = [item.group_id for item in user_groups]

        scopes = {'user:validation'}
        for item in groups_ids:
            scopes.update(set(group_agent.get_scopes_name_list(group_id=item, db=db)))

        return list(scopes)

    @staticmethod
    def get_user_details(page_number: int, page_size: int, **kwargs):
        data = {'result': [], 'total_count': None}

        query = user_crud.get_all_user_details(
            db=kwargs['db'],
            skip=(page_number - 1) * page_size,
            limit=page_size,
            **CqGetUserDetails(**kwargs).dict()
        )
        total_count = query.count()
        result = query.all()

        for user_obj in result:
            data['result'].append(
                {
                    'user_id': user_obj.id,
                    'phone_number': user_obj.mobile,
                    'first_name': user_obj.first_name,
                    'last_name': user_obj.last_name,
                    'verified': user_obj.verified,
                    'created_at': user_obj.created_at,
                }
            )
        data['total_count'] = total_count
        return data

    @staticmethod
    def get_merchant_info_with_login(current_user_id: int, db: Session = SessionLocal()):
        user = UserInterface.find_by_id(user_id=int(current_user_id), db=db)
        from finance.finance_service import FinanceService
        fn_sr = FinanceService()
        bank_profile = fn_sr.bank_profile.find_item_multi(
            db=db,
            merchant_id=user.merchant.id,
            return_first_obj=True,
            raise_not_found_exception=False
        )

        if not bank_profile:
            raise MerchantBankProfileNotFound

        data = {
            'name': user.merchant.name,
            'name_fa': user.merchant.name_fa,
            'logo_address': user.merchant.logo_address,
            'logo_background_color': user.merchant.logo_background_color,
            'bank_account_number': bank_profile.account_no,
            'bank_iban': bank_profile.iban if bank_profile else None,
            'bank_name': bank_profile.bank_name
        }
        return data


user_agent = UserInterface(
    crud=user_crud,
    create_schema=UserCreateSchema,
    update_schema=UserUpdateSchema,
    get_multi_schema=UserGetMultiSchema,
    exception=user_exception
)
