from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from ..models.schemas.user import CreditUserUpdateSchema, CreditUserGetMulti, CreditUserCreateSchema
from ..models.user import credit_user_crud


class UserInterface(InterfaceBase):

    def __init__(
            self,
            crud: CRUDBase,
            create_schema,
            update_schema,
            get_multi_schema
    ):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = crud

    def lock_credit(self, db: Session, user_id):
        pass
        # self.update_item(db=db,
        #                  find_by={'user_id': user_id},
        #                  update_to={'is_locked': True}
        #                  )

    def unlock_credit(self, db: Session, user_id):
        pass
        # self.update_item(db=db,
        #                  find_by={'user_id': user_id},
        #                  update_to={'is_locked': False}
        #                  )


credit_user_agent = UserInterface(
    crud=credit_user_crud,
    create_schema=CreditUserCreateSchema,
    update_schema=CreditUserUpdateSchema,
    get_multi_schema=CreditUserGetMulti
)
