import datetime
from pydantic import BaseModel, Field


class NotificationCenterDetail(BaseModel):
    id: int = \
        Field(...,
              title='id',
              description='id of object',
              example=13
              )
    text: str = \
        Field(...,
              title='text',
              description='text of notification',
              example='a sample text of notification'
              )
    title: str | None = \
        Field(...,
              title='title',
              description='title of notification',
              example='otp code'
              )

    seen_at: datetime.datetime | None = \
        Field(...,
              title='seen at',
              description='seen at',
              example='2023-03-29 10:22:32.929275'
              )

    with_push_notification: bool = \
        Field(...,
              title='has_push_notification',
              description='also has push notification or not',
              example=False
              )

    with_sms: bool = \
        Field(...,
              title='has_sms',
              description='also has sms or not',
              example=True
              )

    send_at: datetime.datetime | None = \
        Field(...,
              title='send at',
              description='send at',
              example='2023-03-29 10:22:32.929275'
              )



class NotificationCenterMeResponse(BaseModel):
    unread_notifications_count: int = \
        Field(...,
              title='unread notifications count',
              description='count of unread notifications',
              example=10
              )

    notifications: list[NotificationCenterDetail]


class NotificationSeenRequest(BaseModel):
    notification_ids: list[int] = \
        Field(...,
              title='notification seen request',
              description='notification seen request',
              example=[1, 2, 10]
              )


class NotificationSeenResponse(BaseModel):
    status: str = \
        Field(...,
              title='status',
              description='it should be Done',
              example="Done"
              )
