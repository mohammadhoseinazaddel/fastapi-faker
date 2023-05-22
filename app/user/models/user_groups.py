from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from system.base.crud import CRUDBase
from system.dbs.models import Base
from user.models.schemas.user_groups import UserGroupsCreateSchema, UserGroupsUpdateSchema, UserGroupsGetMultiSchema


class UsrUserGroups(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    user_id = Column(Integer, ForeignKey('usr_user.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('usr_group.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'group_id', name='user_groups_unique'),
    )


class UserGroupsCRUD(
    CRUDBase[
        UsrUserGroups,
        UserGroupsCreateSchema,
        UserGroupsUpdateSchema,
        UserGroupsGetMultiSchema
    ]
):
    pass


user_groups_crud = UserGroupsCRUD(UsrUserGroups)
