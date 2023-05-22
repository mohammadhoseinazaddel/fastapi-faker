from fastapi import APIRouter, Depends, Security, Query, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from notification.models.notification_center import NtfNotificationCenter

from system.dbs.postgre import get_db
from utils import ResponseManager
from user.interfaces.user import UserInterface

from ...exceptions import NotificationNotFoundException

from ..schemas.center import *

router = APIRouter()

notification_center_me_RM = ResponseManager(
    request_model=None,
    response_model=NotificationCenterMeResponse,
    pagination=True,
    is_mock=False
)


@router.get("/me",
            response_model=notification_center_me_RM.response_model(),
            response_description="Get user notifications When Logged In"
            )
async def get_my_notifications(
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["notification:notification_center:me"]),
        unread_only: bool = False,
        page_number: int = Query(default=1, ge=1)
):
    from notification.notification_service import NotificationService
    notification_sr = NotificationService()
    notifications_result_list = []
    notifications_result = []
    page_size = 10

    try:
        # count of unread notifications
        unread_notification_count, total_count = notification_sr.notification_center.count_of_unread_notifications_and_total_count(
            db=db,
            user_id=current_user_id,
            unread_only=unread_only,
        )

        # notifications
        if unread_only:
            notifications_result_list = notification_sr.notification_center.find_item_multi(
                db=db,
                user_id=current_user_id,
                raise_not_found_exception=False,
                with_push_notification=True,
                seen_at__isnull=unread_only,
                skip=(page_number - 1) * page_size,
                limit=page_size,
                order_by=('id', 'desc')
            )
        else:
            notifications_result_list = notification_sr.notification_center.find_item_multi(
                db=db,
                user_id=current_user_id,
                raise_not_found_exception=False,
                skip=(page_number - 1) * page_size,
                limit=page_size,
                order_by=('id', 'desc')
            )

        notification_center_me_RM.pagination_data(
            total_count=total_count,
            current_page=page_number,
            page_size=10
        )
        for notif in notifications_result_list:
            notifications_result.append({
                'id': notif.id,
                'text': notif.text,
                'title': notif.title,
                'seen_at': notif.seen_at,
                'with_push_notification': notif.with_push_notification,
                'with_sms': notif.with_sms,
                'send_at': notif.created_at
            })
        notification_center_me_RM.status_code(200)
        return notification_center_me_RM.response({
            'unread_notifications_count': unread_notification_count,
            'notifications': notifications_result
        })
    except Exception as e:
        return notification_center_me_RM.exception(e)


notification_center_seen_RM = ResponseManager(
    request_model=NotificationSeenRequest,
    response_model=NotificationSeenResponse,
    pagination=False,
    is_mock=False
)


@router.post("/seen",
             response_model=notification_center_seen_RM.response_model(),
             response_description="Seen notification When Logged In"
             )
async def seen_notification(
        request_model: notification_center_seen_RM.request_model(),
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user,
                                        scopes=["notification:notification_center:seen"]),
):
    from notification.notification_service import NotificationService
    notification_sr = NotificationService()

    try:
        notifications = db.query(NtfNotificationCenter).filter(
            NtfNotificationCenter.id.in_(request_model.notification_ids),
            NtfNotificationCenter.user_id == current_user_id
        ).all()
        if not notifications:
            raise NotificationNotFoundException

        for notification in notifications:
            if not notification.seen_at:
                notification.seen_at = datetime.datetime.now()

        notification_center_seen_RM.status_code(201)
        return notification_center_seen_RM.response(data={'status': "Done"})
    except Exception as e:
        return notification_center_seen_RM.exception(e)


@router.post('/develop/send-notification')
async def send_notification(
        text: str,
        user_id: int,
        push_notification: bool,
        send_sms: bool,
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user,
                                        scopes=["notification:notification_center:send"]),
):
    from notification.notification_service import NotificationService
    if push_notification:
        raise HTTPException(status_code=501, detail="push notification not integrated yet")
    notification_sr = NotificationService()
    notification_sr.notification_center.send(
        user_id=user_id,
        text=text,
        with_push_notification=push_notification,
        with_sms=send_sms,
        input_type='notification-center-test-api',
        title='test-api'
    )
    return JSONResponse(content='ok', status_code=201)
