from sqlalchemy.orm import Session
from system.dbs.postgre import SessionLocal
from ..exceptions.rules import RulesNotFound
from ..models.rules import rules_crud, SoRule
from ..models.schemas.rule import CreateRules


class RulesInterface:
    """
    this class work base on safe delete
    """

    def __init__(self):
        self.base_crud = rules_crud

    def create(self, rules_info: CreateRules, db: Session = SessionLocal()) -> SoRule:
        return self.base_crud.create(db=db, obj_in=rules_info)

    def find_by_id(self, rules_id: int, db: Session = SessionLocal()) -> SoRule:
        pay = self.base_crud.get(db=db, id=rules_id)
        if not pay:
            raise RulesNotFound

        return pay

    def find_all(self, db: Session = SessionLocal()):
        q = self.base_crud.get_multi(db=db)
        return [{"id": i.id, "version": i.version, "rules": i.rules} for i in q]


rules_agent = RulesInterface()
