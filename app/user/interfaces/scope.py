import datetime

from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.dbs.postgre import SessionLocal

from user.models.schemas.scope import ScopeCreateSchema, ScopeUpdateSchema, ScopeGetMultiSchema
from user.models.scope import scope_crud, UsrScope


class ScopeInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)

        self.crud = scope_crud
        self.model = UsrScope

    def create_or_update_scopes_from_dict(self, scope_dict: dict, db: Session = SessionLocal()):
        try:
            for k, v in scope_dict.items():
                if not self.find_item_multi(db=db, raise_not_found_exception=False, name=v['name']):
                    self.add_item(
                        db=db,
                        name=v['name'],
                        fa_name=v['fa_name'] if 'fa_name' in v else None,
                        description=v['description'] if 'description' in v else None,
                        module=v['module'] if 'module' in v else None,
                        interface=v['interface'] if 'interface' in v else None,
                        endpoint=v['endpoint'] if 'endpoint' in v else None,
                        action=v['action'] if 'action' in v else None
                    )

                else:
                    self.update_item(
                        db=db,
                        find_by={'name': v['name']},
                        update_to={
                            'name_fa': v['fa_name'] if 'fa_name' in v else None,
                            'description': v['description'] if 'description' in v else None,
                            "module": v['module'] if 'module' in v else None,
                            'interface': v['interface'] if 'interface' in v else None,
                            "endpoint": v['endpoint'] if 'endpoint' in v else None,
                            "action": v['endpoint'] if 'endpoint' in v else None,
                        }
                    )
            db.commit()
        except Exception as e:
            raise e


scope_agent = ScopeInterface(
    crud=scope_crud,
    create_schema=ScopeCreateSchema,
    update_schema=ScopeUpdateSchema,
    get_multi_schema=ScopeGetMultiSchema
)
