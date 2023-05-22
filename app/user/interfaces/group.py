from typing import List

from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.dbs.postgre import SessionLocal

from user.models.group import UsrGroup, group_crud
from ..interfaces.scope import scope_agent
from user.models.schemas.group import GroupCreateSchema, GroupGetMultiSchema, GroupUpdateSchema
from user.models.group_scopes import UsrGroupScopes, group_scopes_crud
from user.models.schemas.group_scopes import GroupScopesCreateSchema, GroupScopesUpdateSchema, GroupScopesGetMultiSchema


class GroupScopesInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)

        self.model = UsrGroupScopes
        self.crud = group_scopes_crud


group_scopes_agent = GroupScopesInterface(
    crud=group_scopes_crud,
    create_schema=GroupScopesCreateSchema,
    update_schema=GroupScopesUpdateSchema,
    get_multi_schema=GroupScopesGetMultiSchema
)


class GroupInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)

        self.crud = crud
        self.model = UsrGroup
        self.group_scopes = group_scopes_agent

    def set_scopes(
            self,
            group_id: int,
            scope_id_list: List[int] = None,
            scope_name_list: List[str] = None,
            db: Session = SessionLocal()
    ):
        if not scope_id_list:
            if not scope_name_list:
                raise ValueError

            scope_id_list = [x.id for x in scope_agent.crud.get_scopes_instances_from_name_list(db=db, scope_names_list=scope_name_list)]

        exist_scope_ids = self.group_scopes.crud.get_group_scope_ids(group_id=group_id, db=db)

        to_add_scope_ids = [x for x in scope_id_list if x not in exist_scope_ids]
        to_del_scope_ids = [x for x in exist_scope_ids if x not in scope_id_list]

        for item in to_add_scope_ids:
            self.group_scopes.add_item(
                db=db,
                group_id=group_id,
                scope_id=item
            )

        for item in to_del_scope_ids:
            self.group_scopes.delete_item(
                db=db,
                find_by={
                    "group_id": group_id,
                    "scope_id": item
                },
                hard_delete=True
            )

        db.flush()

    def get_scopes_name_list(
            self,
            group_id: int,
            db: Session = SessionLocal()
    ):
        scope_ids = self.group_scopes.crud.get_group_scope_ids(group_id=group_id, db=db)

        return [x.name for x in scope_agent.crud.get_scopes_instances_from_id_list(db=db, scope_id_list=scope_ids)]

    def create_or_update_group(
            self,
            group_name: str,

            scope_name_list: List[str],

            group_fa_name: str = None,
            group_desc: str = None,
            db: Session = SessionLocal()
    ):
        group = self.find_item_multi(
            db=db,
            raise_not_found_exception=False,
            name=group_name
        )
        if not group:
            group = self.add_item(
                db=db,
                name=group_name,
                fa_name=group_fa_name,
                description=group_desc,
            )
        else:
            group = group[0]

        db.flush()

        self.set_scopes(
            group_id=group.id,
            scope_name_list=scope_name_list,
            db=db
        )
        db.commit()


group_agent = GroupInterface(
    crud=group_crud,
    create_schema=GroupCreateSchema,
    update_schema=GroupUpdateSchema,
    get_multi_schema=GroupGetMultiSchema
)
