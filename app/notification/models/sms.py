from typing import Type

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, Boolean

from notification.models.schemas.sms import SmsCreateSchema, SmsUpdateSchema, SmsGetMultiSchema
from system.base.crud import CRUDBase, ModelType
from system.dbs.models import Base


class NtfSms(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    input_type = Column(String, nullable=False)
    input_unique_id = Column(Integer, nullable=True)
    retrying_count = Column(Integer, nullable=False, default=0)
    last_retried = Column(DateTime, nullable=True)
    status = Column(String)
    provider_id = Column(ForeignKey('ntf_provider.id'), nullable=True)
    user_id = Column(Integer, nullable=True)
    mobile_number = Column(String, nullable=False)
    text = Column(String, nullable=False)
    template_id = Column(ForeignKey('ntf_template.id'), nullable=True)
    provider_message_id = Column(String, nullable=True)


class SmsCRUD(
    CRUDBase[
        NtfSms,
        SmsCreateSchema,
        SmsUpdateSchema,
        SmsGetMultiSchema
    ]
):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)
        self.STATUS_READY = 'READY'
        self.STATUS_SENDING = 'SENDING'
        self.STATUS_SENT = 'SENT'
        self.STATUS_FAILED = 'FAILED'


sms_crud = SmsCRUD(NtfSms)
