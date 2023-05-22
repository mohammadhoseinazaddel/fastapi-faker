from sqlalchemy import Column, Integer, String

from system.base.crud import CRUDBase
from system.dbs.models import Base
from system_object.models.schemas.rule import CreateRules, UpdateRules, GetMultiSoRule


class SoRule(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    version = Column(String, nullable=False)
    rules = Column(String(2048), nullable=False)


class RulesCRUD(CRUDBase[SoRule, CreateRules, UpdateRules, GetMultiSoRule]):
    pass


rules_crud = RulesCRUD(SoRule)
