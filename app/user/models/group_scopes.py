from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.dbs.models import Base

from user.models.schemas.group_scopes import GroupScopesCreateSchema, GroupScopesUpdateSchema, GroupScopesGetMultiSchema


class UsrGroupScopes(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    group_id = Column(Integer, ForeignKey('usr_group.id'), nullable=False)
    scope_id = Column(Integer, ForeignKey('usr_scope.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('group_id', 'scope_id', name='group_scopes_unique'),
    )


class GroupScopesCRUD(
    CRUDBase[
        UsrGroupScopes,
        GroupScopesCreateSchema,
        GroupScopesUpdateSchema,
        GroupScopesGetMultiSchema
    ]
):
    def get_group_scope_ids(
            self,
            group_id: int,
            db: Session
    ):
        return [item.scope_id for item in db.query(self.model).filter(self.model.group_id == group_id).all()]


group_scopes_crud = GroupScopesCRUD(UsrGroupScopes)
