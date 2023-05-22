from datetime import datetime

import firebase_admin
from sqlalchemy import case, cast, String
from sqlalchemy.orm import Session
from notification.interfaces.template import template_agent
from notification.models.push_notification import NtfPushNotification, push_notification_crud
from notification.models.schemas.push_notification import PushNotificationCreateSchema, PushNotificationUpdateSchema, \
    PushNotificationGetMultiSchema
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.config import settings
from system.dbs.postgre import SessionLocal

from firebase_admin import credentials, messaging


firebase_cred = credentials.Certificate(settings.FIREBASE_CERTIFICATION)
firebase_app = firebase_admin.initialize_app(firebase_cred)


class PushNotificationInterface(InterfaceBase):

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = crud

    def send_push_notification(
            self,
            token: str,
            input_type: str,
            input_unique_id: int,
            text: str,
            title: str,
            user_id: int = None,
            template_id: int = None,
            **kwargs
    ):
        db = SessionLocal() if not 'db' in kwargs.keys() else kwargs['db']

        self.add_item(
            db=db,
            token=token,
            input_type=input_type,
            input_unique_id=input_unique_id,
            user_id=user_id,
            text=text,
            title=title,
            template_id=template_id
        )
        db.commit()
        db.close()

    def send_push_notification_with_template(
            self,
            input_type: str,
            input_unique_id: int,
            template_name: int,
            template_key_values_dict: dict,
            token: str,
            user_id: int = None
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

        self.send_push_notification(
            token=token,
            input_type=input_type,
            input_unique_id=input_unique_id,
            user_id=user_id,
            text=generated_text,
            template_id=template_id,
            title=title
        )
        db.close()

    def job_send_push_notification_and_update_status_from_ready_to_sending(self, db: Session):
        try:
            list_of_local_message_ids = []  # [12, 13]
            list_of_messages = []  # {'local_message_id': 12, 'provider_message_id': 35235, exception:None, status:SENT}

            # List of messages with ready status
            ready_to_send_messages: list[NtfPushNotification] = self.find_item_multi(
                db,
                status=self.crud.STATUS_READY,
                raise_not_found_exception=False
            )
            if not ready_to_send_messages:
                return None

            # Append all message id (our database id) to "list_of_local_message_ids"
            for message in ready_to_send_messages:
                list_of_local_message_ids.append(message.id)

            # Update status of all received message to "SENDING".
            db.query(NtfPushNotification).filter(
                NtfPushNotification.id.in_(list_of_local_message_ids)
            ).update(
                {
                    NtfPushNotification.status: self.crud.STATUS_SENDING,
                }
            )
            db.commit()

            firebase_messages_list = []

            for message in ready_to_send_messages:
                firebase_messages_list.append(
                    messaging.Message(
                        notification=messaging.Notification(title=message.title, body=message.text),
                        token=message.token
                    )
                )
            batch_response_obj = messaging.send_all(firebase_messages_list)

            # create jsons to update our db
            for index, response in enumerate(batch_response_obj.responses):
                list_of_messages.append(
                    {
                        "local_message_id": list_of_local_message_ids[index],
                        "provider_message_id": str(response.message_id),
                        "exception": str(response.exception),
                        "status": self.crud.STATUS_SENT if response.success else self.crud.STATUS_SENDING
                    }
                )

            # update our db with responses of firebase
            db.query(NtfPushNotification).filter(
                NtfPushNotification.id.in_(list_of_local_message_ids)
            ).update({
                NtfPushNotification.status: case([
                    (cast(NtfPushNotification.id, String) == str(item['local_message_id']), item['status'])
                    for item in list_of_messages
                ], else_="-1"),
                NtfPushNotification.exception: case([
                    (cast(NtfPushNotification.id, String) == str(item['local_message_id']), item['exception'])
                    for item in list_of_messages
                ], else_="-1"),
                NtfPushNotification.provider_message_id: case([
                    (cast(NtfPushNotification.id, String) == str(item['local_message_id']), item['provider_message_id'])
                    for item in list_of_messages
                ], else_="-1")
            }, synchronize_session=False)

            db.commit()
            db.close()

        except Exception as e:
            raise e

    def job_retry(self, db: Session):

        # List of messages with ready status
        messages_with_status_sending: list[NtfPushNotification] = self.find_item_multi(
            db,
            status=self.crud.STATUS_SENDING,
            raise_not_found_exception=False
        )

        if not messages_with_status_sending:
            return

        for message in messages_with_status_sending:
            if message.retrying_count >= 10:
                message.status = self.crud.STATUS_FAILED
                continue
            if (datetime.now() - message.updated_at).seconds > 8:
                message.retrying_count = message.retrying_count + 1
                message.status = self.crud.STATUS_READY

        db.commit()
        db.close()


push_notification_agent = PushNotificationInterface(
    crud=push_notification_crud,
    create_schema=PushNotificationCreateSchema,
    update_schema=PushNotificationUpdateSchema,
    get_multi_schema=PushNotificationGetMultiSchema
)
