from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from utils import ResponseManager
from ..schemas.rules import *

router = APIRouter()

rules_RM = ResponseManager(
    request_model=RulesCreateRequest,
    response_model=RulesIdResponse,
    pagination=False,
    is_mock=False
)


@router.post("/create",
             response_model=rules_RM.response_model(),
             response_description="create rules"
             )
def create_rules(rule_info: rules_RM.request_model(),
                 db: Session = Depends(get_db),
                 # current_user_id: str = Security(AuthInterface.get_current_user, scopes=["blockchain:depositAddress"])
                 ):
    try:
        from system_object import SystemObjectsService
        sys_obj_sr = SystemObjectsService()

        rule = sys_obj_sr.coin.create(db=db, rules_info=rule_info)
        rules_RM.status_code(200)
        return rules_RM.response(rule)

    except Exception as e:
        http_exceptions = []
        if e.__class__.__name__ in http_exceptions:
            return rules_RM.exception(e)
        else:
            raise e


rules_get_all_RM = ResponseManager(
    request_model=RulesCreateRequest,
    response_model=RulesGetResponse,
    pagination=False,
    is_mock=False,
    is_list=True
)


@router.get("/get",
            response_model=rules_get_all_RM.response_model(),
            response_description="Get Rules"
            )
def get_rule(id: int,
             db: Session = Depends(get_db),
             # current_user_id: str = Security(AuthInterface.get_current_user, scopes=["blockchain:depositAddress"])
             ):
    try:
        from system_object import SystemObjectsService
        sys_obj_sr = SystemObjectsService()

        rules_get_all_RM.status_code(200)
        rule = sys_obj_sr.rules.find_by_id(rules_id=id, db=db)
        return rules_get_all_RM.response(rule)

    except Exception as e:
        http_exceptions = ['RulesNotFound']
        if e.__class__.__name__ in http_exceptions:
            return rules_get_all_RM.exception(e)
        else:
            raise e


@router.get("/all",
            response_model=rules_get_all_RM.response_model(),
            response_description="Get All Rules"
            )
def get_all_rules(
        db: Session = Depends(get_db),
        # current_user_id: str = Security(AuthInterface.get_current_user, scopes=["blockchain:depositAddress"])
):
    try:
        from system_object import SystemObjectsService
        sys_obj_sr = SystemObjectsService()

        rules_get_all_RM.status_code(200)
        q = sys_obj_sr.rules.base_crud.get_multi(db=db)
        data = [{"id": i.id, "version": i.version, "rules": i.rules} for i in q]

        return rules_get_all_RM.response(data)

    except Exception as e:
        http_exceptions = []
        if e.__class__.__name__ in http_exceptions:
            return rules_get_all_RM.exception(e)
        else:
            raise e
