from typing import Type

from sqlalchemy import Column, Integer, String
from notification.models.schemas.provider import ProviderCreateSchema, ProviderUpdateSchema, ProviderGetMultiSchema
from system.base.crud import CRUDBase, ModelType
from system.dbs.models import Base


class NtfProvider(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    line_number = Column(String, nullable=False)
    position_number = Column(Integer, nullable=False, unique=True)


class ProviderCRUD(
    CRUDBase[
        NtfProvider,
        ProviderCreateSchema,
        ProviderUpdateSchema,
        ProviderGetMultiSchema
    ]
):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)
        self.STATUS_READY = 'READY'
        self.STATUS_SENDING = 'SENDING'
        self.STATUS_SENT = 'SENT'
        self.STATUS_FAILED = 'FAILED'


provider_crud = ProviderCRUD(NtfProvider)
