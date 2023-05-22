import asyncio
import datetime

from sqlalchemy import case, String, cast, or_, func
from sqlalchemy.orm import Session

from ext_services.kavenegar.interfaces.sms import kavenegar_agent
from notification.interfaces.providers import provider_agent
from notification.interfaces.template import template_agent
from notification.models.providers import NtfProvider
from notification.models.schemas.sms import SmsUpdateSchema, SmsCreateSchema, SmsGetMultiSchema
from notification.models.sms import sms_crud, NtfSms
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.dbs.postgre import SessionLocal


class SmsInterface(InterfaceBase):

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = crud

    def send_sms(
            self,
            mobile_number: str,
            input_type: str,
            input_unique_id: int,
            text: str,
            template_id: int = None,
            user_id: int = None,
            **kwargs
    ):
        db = SessionLocal() if not 'db' in kwargs.keys() else kwargs['db']

        self.add_item(
            db=db,
            mobile_number=mobile_number,
            input_type=input_type,
            input_unique_id=input_unique_id,
            user_id=user_id,
            text=text,
            template_id=template_id
        )
        db.commit()
        db.close()

    def send_sms_with_template(
            self,
            input_type: str,
            input_unique_id: int,
            template_name: int,
            template_key_values_dict: dict,
            mobile_number: str,
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

        self.send_sms(
            input_type=input_type,
            input_unique_id=input_unique_id,
            mobile_number=mobile_number,
            user_id=user_id,
            text=generated_text,
            template_id=template_id
        )
        db.close()

    async def job_send_sms_and_update_status_from_ready_to_sending_async_version(self, db: Session):
        list_of_message = []  # {'message_id': 12, 'provider_message_id': 3325235}
        list_of_local_message_ids = []  # [12, 13]

        # List of all providers order by position_number
        providers: list[NtfProvider] = provider_agent.find_item_multi(db=db, order_by=('position_number', 'desc'))

        # List of messages with ready status
        ready_to_send_messages: list[NtfSms] = self.find_item_multi(
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
        db.query(NtfSms).filter(
            NtfSms.id.in_(list_of_local_message_ids)
        ).update(
            {
                NtfSms.status: self.crud.STATUS_SENDING,
            }
        )
        # self.update_item(db=db, find_by={'status': "READY"}, update_to={'status': self.crud.STATUS_SENDING})
        db.commit()

        tasks = []  # Add sending messages to task queue and execute them asynchronously
        for message in ready_to_send_messages:
            # Send message for first time
            if not message.retrying_count:
                to_send_provider = providers[0]  # first provider
                if to_send_provider.name == 'kavenegar':
                    tasks.append(asyncio.create_task(kavenegar_agent.send_sms(
                        receptor=message.mobile_number,
                        message=message.text,
                        line_number=to_send_provider.line_number,
                        local_message_id=message.id,
                        provider_id=to_send_provider.id
                    )))

            if message.retrying_count and message.retrying_count < 11:
                # Retry message
                to_send_provider = providers[
                    (message.retrying_count - 1) % len(providers)]  # to choose provider to send based on retrying count
                if to_send_provider.name == 'kavenegar':
                    tasks.append(asyncio.create_task(kavenegar_agent.send_sms(
                        receptor=message.mobile_number,
                        message=message.text,
                        line_number=to_send_provider.line_number,
                        local_message_id=message.id,
                        provider_id=to_send_provider.id
                    )))

        # Execute tasks
        responses = await asyncio.gather(*tasks)

        for response in responses:
            list_of_message.append(
                {
                    'local_message_id': response[1],
                    'provider_message_id': response[0]['entries'][0]['messageid'],
                    'provider_id': response[2]
                }
            )

        db.query(NtfSms).filter(
            NtfSms.id.in_(list_of_local_message_ids)
        ).update({
            NtfSms.provider_message_id: case([
                (cast(NtfSms.id, String) == str(item['local_message_id']), item['provider_message_id'])
                for item in list_of_message
            ], else_=-1),
            NtfSms.provider_id: case([
                (cast(NtfSms.id, String) == str(item['local_message_id']), item['provider_id'])
                for item in list_of_message
            ], else_=-1),
            NtfSms.last_retried: case([
                (cast(NtfSms.id, String) == str(item['local_message_id']), datetime.datetime.now())
                for item in list_of_message
            ])
        }, synchronize_session=False)
        db.commit()
        db.close()

    def job_inquiry(self, db: Session):
        """
            This job will inquiry the messages to get their status
        """
        kavenegar_message_ids = []
        list_messages_local_ids = []

        # Get list of messages with status "SENDING" an inquiry them
        messages_to_inquiry: list[NtfSms] = self.find_item_multi(
            db=db,
            raise_not_found_exception=False,
            status='SENDING'
        )
        for message in messages_to_inquiry:
            list_messages_local_ids.append(message.id)

        # The status is being updated to "INQUIRING" to prevent receiving the message agein(before inquiring)
        # while the job is running continuously.
        # In fact this status is function scope, and it's not in our state machine
        db.query(NtfSms).filter(
            NtfSms.id.in_(list_messages_local_ids)
        ).update(
            {
                NtfSms.status: 'INQUIRING',  # this status is not for the status machine is just function scope

            }
        )
        db.commit()

        providers: list[NtfProvider] = provider_agent.find_item_multi(db=db)
        if not messages_to_inquiry:
            return
        for message in messages_to_inquiry:
            provider_name = None
            for provider in providers:
                if message.provider_id == provider.id:
                    provider_name = provider.name
            if provider_name == 'kavenegar':
                kavenegar_message_ids.append(message.provider_message_id)
        kavenegar_response = kavenegar_agent.check_status(message_ids=kavenegar_message_ids)
        # print("^"*100, kavenegar_response, kavenegar_response.json())
        db.query(NtfSms).filter(
            NtfSms.id.in_(list_messages_local_ids)
        ).update({
            NtfSms.status: case([
                (cast(NtfSms.provider_message_id, String) == str(item['messageid']),
                 kavenegar_agent.map_kavenegar_status_code_to_our_statuses(code=int(item['status'])))
                for item in kavenegar_response.json()['entries']
            ], else_='Not in types')
        }, synchronize_session=False)
        db.commit()
        db.close()

    def job_retry(self, db: Session):
        to_retry_messages = db.query(NtfSms).filter(
            or_(
                NtfSms.status == self.crud.STATUS_SENDING,
                NtfSms.status == self.crud.STATUS_FAILED
            ),
            NtfSms.retrying_count.between(0, 9),
            # func.extract('epoch', func.now() - NtfSms.created_at) > (NtfSms.retrying_count * 10 + 10)
            func.extract('epoch', func.now() - NtfSms.last_retried) > 10

        )
        for message in to_retry_messages:
            message.status = self.crud.STATUS_READY
            message.retrying_count += 1
        db.commit()
        db.close()


sms_agent = SmsInterface(
    crud=sms_crud,
    create_schema=SmsCreateSchema,
    update_schema=SmsUpdateSchema,
    get_multi_schema=SmsGetMultiSchema
)
