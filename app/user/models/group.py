from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.dbs.models import Base

from .schemas.group import GroupCreateSchema, GroupUpdateSchema, GroupGetMultiSchema


class UsrGroup(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    fa_name = Column(String)
    description = Column(String, nullable=True, )


class GroupCRUD(
    CRUDBase[
        UsrGroup,
        GroupCreateSchema,
        GroupUpdateSchema,
        GroupGetMultiSchema
    ]
):
    def get_group_instances_from_name_list(self, db: Session, group_names_list: list):
        return db.query(self.model).filter(self.model.name.in_(group_names_list))


group_crud = GroupCRUD(UsrGroup)
