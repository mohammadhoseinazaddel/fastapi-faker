import datetime

from typing import List

import requests

from ext_services.jibit.transferor.shemas.transfer import Transfer
from ext_services.jibit.transferor.token import jibit_transferor_get_token
from system.config import settings


class JibitTransferorInterface:

    def _jibit_transfer_batch(
            self,
            transfers: List[Transfer],
            batch_id: str,
    ):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + settings.JIBIT_TRANSFEROR_ACCESS_TOKEN
        }

        to_send_transfers = []
        for item in transfers:
            transfer = {
                'transferID': str(item.transfer_id),
                'transferMode': item.transfer_mode if item.transfer_mode else 'ACH',
                # optional transfer mode of ACH, NORMAL or RTGS. default is ACH
                # '''
                #     بر اساس استعلام تلفنی از خانم حسین پور:
                #     ACH: پایا,
                #     NORMAL: حساب به حساب,
                #     RTGS: ساتنا (تو لحظه توسعه، این مورد رو سرویس نمیدن)
                # '''

                'destination': item.destination_IBAN,  # destination IBAN
                'destinationFirstName': item.destination_first_name,  # optional
                'destinationLastName': item.destination_last_name,  # optional
                'amount': item.amount,
                'currency': 'IRR',  # 'IRR', 'RIALS', 'TOMAN'
                'description': item.description,
                'metadata': item.metadata,  # optional
                'notifyURL': item.notify_url,  # optional
                'cancellable': item.cancellable if item.cancellable else False,  # optional, default: True
                'paymentID': str(item.payment_id) if item.payment_id else None,
                # optional  احتمالا یه چیزی تو مایه های شناسه پرداخت باشه
            }
            to_send_transfers.append(transfer)
        json_data = {
            'batchID': str(batch_id),
            'submissionMode': "BATCH",  # BATCH or TRANSFER
            #  اگر مقدار این فیلد BATCH قرار داده شود، باید یا همه تراکنش های پرداخت کامل موفق باشد یا هیچ یک انجام نشود
            'transfers': to_send_transfers,
        }

        try:

            response = requests.post(
                settings.JIBIT_TRANSFEROR_BASE_URL + '/v2/transfers',
                headers=headers,
                json=json_data
            )
            if 'code' in response.json():
                if response.json()['code'] == 403:
                    jibit_transferor_get_token()
                return self._jibit_transfer_batch(
                    transfers=transfers,
                    batch_id=batch_id
                )

            if 'errors' in response.json():
                for item in response.json()['errors']:
                    if item.get('httpStatusCode') == 403:
                        jibit_transferor_get_token()
                        return self._jibit_transfer_batch(
                            transfers=transfers,
                            batch_id=batch_id
                        )
            return response.json()


        except Exception as e:
            raise ConnectionError

        # ''' Possible errors based on jibit document
        #     'forbidden',
        #     'invalid.request_body',
        #     'batchID.invalid_length',
        #     'submissionMode.not_valid',
        #     'transfers.invalid_length',
        #     'transfers.i.transferID.invalid_length', # (ith item in batch has issue)
        #     'transfers.i.destination.not_valid',
        #     'transfers.i.source_bank.not_supported',
        #     'transfers.i.destinationFirstName.invalid_length',
        #     'transfers.i.destinationLastName.invalid_length',
        #     'transfers.i.amount.not_enough_for_ach',
        #     'transfers.i.amount.exceeded_maximum_for_ach',
        #     'transfers.i.amount.not_enough_for_normal',
        #     'transfers.i.amount.exceeded_maximum_for_normal',
        #     'transfers.i.currency.not_valid',
        #     'transfers.i.description.invalid_length',
        #     'transfers.i.metadata.invalid_length',
        #     'transfers.i.notifyURL.invalid_length',
        #     'transfers.i.notifyURL.not_valid',
        #     'transfers.i.paymentID.invalid_length',
        #     'transfers.i.paymentID.not_valid',
        #     'balances.not_enough',
        #     'transfer.already_exists',
        #     'server.error'
        # '''
        #
        # if 'errors' in response:
        #     for item in response['errors']:
        #         if item['code'].startswith('transfers'):
        #             raise JibitTransferorError(jibit_message=item['code'])
        #
        #         elif item['code'] in ['forbidden']:
        #             raise JibitTransferorCredentialError
        #
        #         elif item['code'] in [
        #             'forbidden',
        #             'invalid.request_body',
        #             'batchID.invalid_length',
        #             'submissionMode.not_valid',
        #             'transfers.invalid_length',
        #         ]:
        #             raise JibitTransferorCompatibilityError(jibit_message=item['code'])
        #
        #         elif item['code'] == 'balances.not_enough':
        #             raise JibitTransferorBalanceNotEnough
        #
        #         elif item['code'] == 'transfer.already_exists':
        #             raise JibitTransferorTransferAlreadyExists
        #
        #         elif item['code'] == 'server.error':
        #             raise JibitTransferorServerError
        #
        #         else:
        #             raise JibitTransferorUndefinedError

    def send_one_transfer(
            self,
            batch_id: str,
            transfer_id: str,
            destination_IBAN: str,
            amount: int,
            description: str,
            transfer_mode: str = None,
            destination_first_name: str = None,
            destination_last_name: str = None,
            metadata: dict = None,
            notify_url: str = None,
            cancellable: bool = None,
            payment_id: str = None,
    ):
        try:
            transfer = Transfer(
                transfer_id=transfer_id,
                transfer_mode=transfer_mode,
                destination_IBAN=destination_IBAN,
                destination_first_name=destination_first_name,
                destination_last_name=destination_last_name,
                amount=amount,
                description=description,
                metadata=metadata,
                notify_url=notify_url,
                cancellable=cancellable,
                payment_id=payment_id
            )
            res = self._jibit_transfer_batch(
                transfers=[transfer],
                batch_id=batch_id,
            )

            if 'submittedCount' in res and res['submittedCount'] == 1:
                return {"status": "successful", 'error_message': None}
            else:
                return {"status": "failed", 'error_message': str(res['errors'])}
        except Exception as e:
            raise e


jibit_transferor_agent = JibitTransferorInterface()
