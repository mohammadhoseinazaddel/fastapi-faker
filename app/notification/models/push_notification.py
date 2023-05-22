from typing import Type

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, Boolean

from notification.models.schemas.push_notification import PushNotificationUpdateSchema, PushNotificationCreateSchema, \
    PushNotificationGetMultiSchema
from system.base.crud import CRUDBase, ModelType
from system.dbs.models import Base


class NtfPushNotification(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    input_type = Column(String, nullable=False)
    input_unique_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    retrying_count = Column(Integer, nullable=False, default=0)
    status = Column(String)  # READY, SENT
    user_id = Column(Integer, nullable=True)
    token = Column(String, nullable=False)  # client token
    text = Column(String, nullable=False)
    template_id = Column(ForeignKey('ntf_template.id'), nullable=True)
    exception = Column(String, nullable=True)
    provider_message_id = Column(String, nullable=True)


class PushNotificationCRUD(
    CRUDBase[
        NtfPushNotification,
        PushNotificationCreateSchema,
        PushNotificationUpdateSchema,
        PushNotificationGetMultiSchema
    ]
):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)
        self.STATUS_READY = 'READY'
        self.STATUS_SENDING = 'SENDING'
        self.STATUS_SENT = 'SENT'
        self.STATUS_FAILED = 'FAILED'


push_notification_crud = PushNotificationCRUD(NtfPushNotification)
