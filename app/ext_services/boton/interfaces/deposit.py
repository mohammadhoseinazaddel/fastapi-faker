from sqlalchemy.orm import Session
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase

from ..models.deposit import (CreateDeposit, GetMultiDeposit, UpdateDeposit,
                              deposit_crud)


class DepositInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = deposit_crud

        self.STATUS_REGISTERED = 'REGISTERED'
        self.STATUS_UPDATED = 'UPDATED'
        self.STATUS_INCREASED = 'INCREASED'
        self.STATUS_UNKNOWN = 'UNKNOWN'

    def get_not_increase_record(self, db: Session):
        records = []
        register_items = self.find_item_multi(db=db, system_status=self.STATUS_REGISTERED,
                                              raise_not_found_exception=False)
        if register_items:
            for item in register_items:
                records.append(item)
        updated_items = self.find_item_multi(db=db, system_status=self.STATUS_UPDATED, raise_not_found_exception=False)
        if updated_items:
            for item in updated_items:
                records.append(item)
        return records


deposit_agent = DepositInterface(
    crud=deposit_crud,
    create_schema=CreateDeposit,
    update_schema=UpdateDeposit,
    get_multi_schema=GetMultiDeposit
)
