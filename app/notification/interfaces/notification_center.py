from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from notification.interfaces.push_notification import push_notification_agent
from notification.interfaces.template import template_agent
from notification.models.notification_center import notification_center_crud, NtfNotificationCenter
from notification.models.schemas.notification_center import NotificationCenterCreateSchema, \
    NotificationCenterUpdateSchema, NotificationCenterGetMultiSchema
from system.base.crud import CRUDBase
from system.base.exceptions import Error
from system.base.interface import InterfaceBase
from system.dbs.postgre import SessionLocal
from user.interfaces.user import UserInterface


class NotificationCenterInterface(InterfaceBase):

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = crud

    def send(
            self,
            user_id: int,
            text: str,
            with_push_notification: bool = False,
            with_sms: bool = False,
            input_type: str = None,
            input_unique_id: int = None,
            title: str = None,
            template_id: int = None,
            **kwargs
    ):
        from notification.notification_service import NotificationService
        notification_center_sr = NotificationService()

        from user import UserService
        user_sr = UserService()

        if not (with_sms or with_push_notification):
            raise SystemError("choose at least one of notification services")

        if with_push_notification:
            if not title:
                raise SystemError("push notification should have title")

        db = SessionLocal() if not 'db' in kwargs.keys() else kwargs['db']

        created_obj = self.add_item(
            db=db,
            input_type=input_type,
            input_unique_id=input_unique_id,
            user_id=user_id,
            text=text,
            title=title,
            template_id=template_id,
            with_push_notification=with_push_notification,
            with_sms=with_sms
        )
        db.commit()

        user_obj = user_sr.user.find_item_multi(db=db, id=user_id, return_first_obj=True)

        if not user_obj.mobile:
            raise HTTPException(status_code=422, detail="User dont have mobile number")

        if with_sms:
            notification_center_sr.sms.send_sms(
                mobile_number=user_obj.mobile,
                input_type='notification-center',
                input_unique_id=created_obj.id,
                text=text,
                user_id=user_id
            )
        if with_push_notification:
            tokens = UserInterface.get_list_of_user_firebase_token(user_id=user_id)
            if tokens:
                for token in tokens:
                    push_notification_agent.send_push_notification(
                        token=token,
                        input_type='notification_center',
                        input_unique_id=created_obj.id,
                        text=text,
                        title=title,
                        user_id=user_id
                    )
        db.close()

    def send_with_template(
            self,
            template_name: str,
            template_key_values_dict: dict,
            user_id: int,
            with_push_notification: bool = False,
            with_sms: bool = False,
            input_type: str = None,
            input_unique_id: int = None,
    ):

        db = SessionLocal()
        generated_text_and_template_id = template_agent.generate_text_with_template_name(
            db=db,
            template_name=template_name,
            key_value_dict=template_key_values_dict
        )
        generated_text = generated_text_and_template_id[0]
        template_id = generated_text_and_template_id[1]
        title = generated_text_and_template_id[2]

        self.send(
            user_id=user_id,
            text=generated_text,
            with_push_notification=with_push_notification,
            with_sms=with_sms,
            input_type=input_type,
            input_unique_id=input_unique_id,
            title=title,
            template_id=template_id,
            db=db
        )
        db.commit()
        db.close()

    def count_of_unread_notifications_and_total_count(
            self,
            db: Session,
            user_id: int,
            unread_only: bool
    ):
        try:
            unread_count = db.query(NtfNotificationCenter).filter(
                NtfNotificationCenter.seen_at == None,
                NtfNotificationCenter.with_push_notification == True,
                NtfNotificationCenter.user_id == user_id,

            ).count()

            if unread_only:
                total_count = db.query(NtfNotificationCenter).filter(
                    NtfNotificationCenter.user_id == user_id,
                    NtfNotificationCenter.seen_at == None,
                    NtfNotificationCenter.with_push_notification == True,
                ).count()

            else:
                total_count = db.query(NtfNotificationCenter).filter(
                    NtfNotificationCenter.user_id == user_id
                ).count()
            return unread_count, total_count
        except Exception as e:
            raise e


notification_center_agent = NotificationCenterInterface(
    crud=notification_center_crud,
    create_schema=NotificationCenterCreateSchema,
    update_schema=NotificationCenterUpdateSchema,
    get_multi_schema=NotificationCenterGetMultiSchema
)
