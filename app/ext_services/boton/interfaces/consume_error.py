from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase

from ..models.consume_error import consume_error_crud, CreateConsumeError, UpdateConsumeError, GetMultiConsumeError


class ConsumeErrorInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = consume_error_crud


consume_error_agent = ConsumeErrorInterface(
    crud=consume_error_crud,
    create_schema=CreateConsumeError,
    update_schema=UpdateConsumeError,
    get_multi_schema=GetMultiConsumeError
)
