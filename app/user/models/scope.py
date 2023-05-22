from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.dbs.models import Base

from user.models.schemas.scope import ScopeCreateSchema, ScopeUpdateSchema, ScopeGetMultiSchema


class UsrScope(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, unique=True)
    fa_name = Column(String)
    description = Column(String, nullable=True, )

    module = Column(String)
    interface = Column(String)
    endpoint = Column(String)
    action = Column(String)


class ScopeCRUD(
    CRUDBase[
        UsrScope,
        ScopeCreateSchema,
        ScopeUpdateSchema,
        ScopeGetMultiSchema
    ]
):
    def get_scopes_instances_from_name_list(self, db: Session, scope_names_list: List[str]):
        return db.query(self.model).filter(self.model.name.in_(scope_names_list))

    def get_scopes_instances_from_id_list(self, db: Session, scope_id_list: List[int]):
        return db.query(self.model).filter(self.model.id.in_(scope_id_list))


scope_crud = ScopeCRUD(UsrScope)
