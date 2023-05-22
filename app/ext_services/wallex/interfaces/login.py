import datetime
from sqlalchemy.orm import Session

from system.config import settings
from system.dbs.postgre import SessionLocal
from system.base.interface import InterfaceBase
from system.base.crud import CRUDBase

from ..oauth.schemas.wallex_user_info import WallexUserInfo
from ..exceptions.oauth import WallexError, WallexStateNotFound, WallexLoginTimeExpired
from ..models.schemas.user_login import CreateWallexLogin, GetMultiUsrWlxState, UpdateWallexLogin
from ..models.user_login import wallex_user_crud, WlxLogin
from ..oauth.get_token import wallex_get_token_by_code
from ..oauth.get_login_url import wallex_get_oauth_url
from ..oauth.get_user_info import wallex_get_user_info


class WallexOauthInterface(InterfaceBase):

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = wallex_user_crud

    def create_wallex_login_request(self, db: Session, order_uuid: str = None) -> WlxLogin:
        record = self.add_item(db=db, order_uuid=order_uuid)
        # onj_in = CreateWallexLogin(order_uuid=order_uuid)
        # record = self.crud.create(db=db, obj_in=onj_in)
        url = wallex_get_oauth_url(record.state)
        self.update_item(db=db, find_by={'id': record.id}, update_to={'wallex_login_url': url})
        # record.wallex_login_url = url
        return record

    def get_wallex_token_by_code(self, db: Session, state: str, code: str):
        token = wallex_get_token_by_code(code)
        self.update_item(db=db, find_by={'state': state}, update_to={
            "access_token": token['result']['access_token'],
            "refresh_token": token['result']['refresh_token'],
            "expire_in": token['result']['expires_in'],
        })
        return self.find_item_multi(db=db, state=state)[0].access_token

    def get_wallex_user(self, db: Session, access_token: str) -> WallexUserInfo:
        wallex_user_info = wallex_get_user_info(token=access_token)
        self.update_item(db=db, find_by={'access_token': access_token}, update_to={
            "wallex_user_id": wallex_user_info.wallex_user_id,
            "kyc_level": wallex_user_info.kyc_level
        })
        return wallex_user_info

    @staticmethod
    def get_wallex_user_info(db: Session, access_token: str) -> WallexUserInfo:
        return wallex_get_user_info(token=access_token)

    def find_by_state_for_login(self, state: str, db: Session, ) -> WlxLogin:
        try:
            queryset = self.find_item_multi(db=db, state=state)
            if not queryset:
                raise WallexStateNotFound

            record = queryset[0]
            if (datetime.datetime.now() - record.updated_at).seconds > settings.WALLEX_MAX_SECONDS_FOR_LOGIN * 60:
                raise WallexLoginTimeExpired

            return record

        except Exception as e:
            db.rollback()
            raise e


wallex_login_agent = WallexOauthInterface(
    crud=wallex_user_crud,
    create_schema=CreateWallexLogin,
    update_schema=UpdateWallexLogin,
    get_multi_schema=GetMultiUsrWlxState
)
