
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.config import settings
from system.dbs.postgre import SessionLocal

from ..models.schemas.session import SessionCreateSchema, SessionUpdateSchema, SessionGetMultiSchema
from ..models.session import UsrSession, session_crud


class SessionInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)

        self.crud = crud
        self.model = UsrSession


session_agent = SessionInterface(
    crud=session_crud,
    create_schema=SessionCreateSchema,
    update_schema=SessionUpdateSchema,
    get_multi_schema=SessionGetMultiSchema
)
