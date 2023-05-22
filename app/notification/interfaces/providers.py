from notification.models.providers import provider_crud
from notification.models.schemas.provider import ProviderCreateSchema, ProviderUpdateSchema, ProviderGetMultiSchema
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase


class ProviderInterface(InterfaceBase):

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = crud


provider_agent = ProviderInterface(
    crud=provider_crud,
    create_schema=ProviderCreateSchema,
    update_schema=ProviderUpdateSchema,
    get_multi_schema=ProviderGetMultiSchema
)
