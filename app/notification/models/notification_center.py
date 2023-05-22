from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime

from notification.models.schemas.notification_center import NotificationCenterCreateSchema, \
    NotificationCenterUpdateSchema, NotificationCenterGetMultiSchema
from system.base.crud import CRUDBase
from system.dbs.models import Base


class NtfNotificationCenter(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    input_type = Column(String, nullable=True)
    input_unique_id = Column(Integer, nullable=True)
    with_push_notification = Column(Boolean, nullable=True)
    with_sms = Column(Boolean, nullable=True)
    text = Column(String, nullable=False)
    template_id = Column(ForeignKey('ntf_template.id'), nullable=True)
    title = Column(String, nullable=True)
    user_id = Column(Integer, nullable=True)
    seen_at = Column(DateTime, nullable=True)


class NotificationCenterCRUD(
    CRUDBase[
        NtfNotificationCenter,
        NotificationCenterCreateSchema,
        NotificationCenterUpdateSchema,
        NotificationCenterGetMultiSchema
    ]
):
    pass



notification_center_crud = NotificationCenterCRUD(NtfNotificationCenter)
