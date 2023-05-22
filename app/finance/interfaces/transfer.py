from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from ext_services.jibit.interfaces.transfer import jibit_transferor_agent
from finance.api.v1.schemas.finance_admin import CqGetTransferList
from ext_services.jibit.interfaces.transfer import jibit_transferor_agent
from finance.interfaces.bank_profile import bank_profile_agent
from finance.models.schemas.transfer import TransferCreate, TransferUpdate, TransferGetMulti
from finance.models.transfer import transfer_crud, FncTransfer
from system.base.crud import CRUDBase
from system.base.exceptions import Error
from system.base.interface import InterfaceBase
from system.dbs.postgre import SessionLocal


class TransferInterface(InterfaceBase):

    def __init__(
            self,
            crud: CRUDBase,
            create_schema,
            update_schema,
            get_multi_schema
    ):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = transfer_crud
        self.model = FncTransfer

    def get_with_id_list_query_set(
            self,
            id_list: List[int],
            db: Session = SessionLocal()
    ):
        return db.query(self.model).filter(self.model.id.in_(id_list))

    def get_with_id_list(
            self,
            id_list: List[int],
            db: Session = SessionLocal()
    ):
        return self.get_with_id_list_query_set(id_list, db).all()

    def get_transfers_list(self, page_number: int, page_size: int, **kwargs):
        data = {'result': [], 'total_count': None}

        result = self.crud.get_all_transfers(
            db=kwargs['db'],
            skip=(page_number - 1) * page_size,
            limit=page_size,
            **CqGetTransferList(**kwargs).dict()
        )
        query_result, total_count = result['query_result'], result['total_count']

        for item in query_result:
            transfer_obj = item[0]
            bank_data = item[1]
            data['result'].append(
                {
                    'id': transfer_obj.id,
                    'created_at': transfer_obj.created_at,
                    'type': transfer_obj.type,
                    'bank_transfer_id': transfer_obj.transfer_id,
                    'bank_name': bank_data.bank_name,
                    'account_no': bank_data.account_no,
                    'amount': transfer_obj.amount,
                    'iban': bank_data.iban,
                }
            )
        data['total_count'] = total_count
        return data

    def paya_transfer(
            self,
            bank_profile_id: int,
            amount: int,
            description: str,
            input_type: str,
            input_unique_id: int,
    ):
        """
            This method only do one transfer
        """
        from notification.notification_service import NotificationService

        my_session = SessionLocal()
        notification_sr = NotificationService()

        bank_profile_obj = bank_profile_agent.find_item_multi(db=my_session, id=bank_profile_id)[0]

        transfer_obj = self.add_item(
            db=my_session,
            bank_profile_id=bank_profile_id,
            type='PAYA',
            amount=amount,
            description=description,
            ext_service_name='jibit',
            input_type=input_type,
            input_unique_id=input_unique_id,
        )

        try:

            res = jibit_transferor_agent.send_one_transfer(
                batch_id=transfer_obj.batch_id,
                transfer_id=str(transfer_obj.transfer_id),
                destination_IBAN=bank_profile_obj.iban,
                amount=amount,
                description=description,
                transfer_mode="ACH",
            )

            if res['status'] == 'successful':
                self.update_item(
                    db=my_session,
                    find_by={'id': transfer_obj.id},
                    update_to={"status": 'successful'}
                )

                my_session.commit()
                my_session.close()

                return {"status": res['status'], 'amount': amount}

            else:
                self.update_item(
                    db=my_session,
                    find_by={'id': transfer_obj.id},
                    update_to={"status": 'failed', 'error_message': res['error_message']})

                notification_sr.sms.send_sms(
                    mobile_number='09105041385',
                    input_type='error',
                    input_unique_id=99,
                    text="paya transfer error: " + res['error_message']
                )
                notification_sr.sms.send_sms(
                    mobile_number='09123492501',
                    input_type='error',
                    input_unique_id=99,
                    text="paya transfer error" + res['error_message']
                )

            my_session.commit()
            my_session.close()

            # raise paya transfer error
            class PayaTransferError(Error):
                def __init__(self, ):
                    super().__init__(
                        message="Paya transfer error failed",
                        errors={
                            'code': 422,
                            'message': 'متاسفانه ارسال درخواست برداشت با خطا مواجه شد.',
                        }
                    )

            raise PayaTransferError

        except Exception as e:
            raise e


transfer_agent = TransferInterface(
    crud=transfer_crud,
    create_schema=TransferCreate,
    update_schema=TransferUpdate,
    get_multi_schema=TransferGetMulti
)
