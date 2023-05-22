import json
import threading
from typing import Literal

import pika

from system.config import settings
from system.dbs.postgre import SessionLocal
from .consume_error import consume_error_agent
from .deposit import deposit_agent


class ConsumerThread(threading.Thread):
    def __init__(
            self,
            consume_type=Literal["deposit", "withdraw"],
            withdraw_type=Literal["ACK", "VERIFY", None],
            network=Literal["BITCOIN", "TRC20", "ERC20", None],
            *args,
            **kwargs
    ):
        super(ConsumerThread, self).__init__(*args, **kwargs)
        self._consume_type = consume_type
        self._withdraw_type = withdraw_type
        self._network = network
        self._queue = 'newTx' if self._consume_type == 'deposit' else f'alpha_{self._withdraw_type}_{self._network}'

    def callback_func(self, ch, method, properties, body):
        try:

            json_body = json.loads(body)

            from user_assets import UserAssetsService
            user_asset_sr = UserAssetsService()

            if self._queue in [
                'alpha_ACK_BITCOIN',
                'alpha_ACK_TRC20',
                'alpha_ACK_ERC20',
            ]:
                unique_id = json_body['uniqueId'] if 'uniqueId' in json_body else None
                tx_id = json_body['txId'] if 'txId' in json_body else None
                bundle_id = json_body['bundleId'] if 'bundleId' in json_body else None
                status = json_body['status'] if 'status' in json_body else None

                db = SessionLocal()

                withdraw_rec = user_asset_sr.wallet.crypto_withdraw.find_item_multi(
                    db=db,
                    unique_id=unique_id,
                    raise_not_found_exception=False
                )

                if withdraw_rec:
                    withdraw_rec = withdraw_rec[0]
                    user_asset_sr.wallet.crypto_withdraw.acknowledge_withdraw_request(
                        network=self._network,
                        unique_id=unique_id,
                        tx_id=tx_id,
                        bundle_id=bundle_id,
                        boton_ack_status=status,
                        db=db
                    )

                    db.commit()

                    # acknowledge the message
                    ch.basic_ack(method.delivery_tag)

            elif self._queue in [
                'alpha_VERIFY_BITCOIN',
                'alpha_VERIFY_TRC20',
                'alpha_VERIFY_ERC20',
            ]:

                unique_id = json_body['uniqueId'] if 'uniqueId' in json_body else None
                is_identical = json_body['isIdentical'] if 'isIdentical' in json_body else None
                bundle_id = json_body['bundleId'] if 'bundleId' in json_body else None
                status = json_body['status'] if 'status' in json_body else None
                fee = json_body['fee'] if 'fee' in json_body else None

                db = SessionLocal()

                withdraw_rec = user_asset_sr.wallet.crypto_withdraw.find_item_multi(
                    db=db,
                    unique_id=unique_id,
                    raise_not_found_exception=False
                )

                if withdraw_rec:
                    withdraw_rec = withdraw_rec[0]
                    user_asset_sr.wallet.crypto_withdraw.verify_withdraw_request(
                        unique_id=unique_id,
                        bundle_id=bundle_id,
                        fee=fee,
                        is_identical=is_identical,
                        boton_verify_status=status,
                        db=db
                    )

                    db.commit()

                    # acknowledge the message
                    ch.basic_ack(method.delivery_tag)

            elif self._queue in [
                'newTx'
            ]:
                coin = json_body['coin'] if 'coin' in json_body else None,
                network = json_body['network'],
                amount_str = json_body['amount'] if 'amount' in json_body else None,
                amount_decimal = json_body['decimals'] if 'decimals' in json_body else None,
                confirmation = json_body['confirmation'] if 'confirmation' in json_body else None,  # 616
                boton_status = json_body['status'],  # 0: PENDING, 1: CONFIRMED
                tx_id = json_body['txId'],
                address = json_body['walletAddress'] if 'walletAddress' in json_body else None,
                memo = json_body['memo'] if 'memo' in json_body else None

                if coin:
                    coin = coin[0]

                if network:
                    network = network[0]

                if amount_str:
                    amount_str = amount_str[0]

                if amount_decimal:
                    amount_decimal = amount_decimal[0]

                if confirmation:
                    confirmation = confirmation[0]

                if boton_status:
                    boton_status = boton_status[0]

                if tx_id:
                    tx_id = tx_id[0]

                if address:
                    address = address[0]

                if memo:
                    memo = memo[0]

                db = SessionLocal()
                record = deposit_agent.find_item_multi(
                    db=db,
                    tx_id=tx_id,
                    memo=memo,
                    raise_not_found_exception=False
                )

                if record:
                    record = record[0]
                    if not record.system_status == 'INCREASED':
                        if not record.status == 1:
                            deposit_agent.update_item(
                                db=db,
                                find_by={"id": record.id},
                                update_to={
                                    "confirmation": confirmation,
                                    "status": boton_status,
                                    "system_status": deposit_agent.STATUS_UPDATED
                                }
                            )
                    # acknowledge the message
                    ch.basic_ack(method.delivery_tag)
                else:
                    if address is not None:
                        system_address = user_asset_sr.wallet.address.find_item_multi(
                            db=db,
                            address=address,
                            raise_not_found_exception=False
                        )
                        if system_address:
                            system_address = system_address[0]
                            deposit_agent.add_item(
                                db=db,
                                coin=coin,
                                network=network,
                                amount=amount_str,
                                decimals=amount_decimal,
                                confirmation=confirmation,
                                status=boton_status,
                                tx_id=tx_id,
                                memo=memo,
                                wallet_address=system_address.address
                            )
                            # acknowledge the message
                            ch.basic_ack(method.delivery_tag)

                db.commit()

        except Exception as e:
            try:
                db = SessionLocal()
                consume_error_agent.add_item(
                    db=db,
                    queue=self._queue,
                    body=str(body),
                    error=str(e)
                )
                db.commit()
                ch.basic_ack(method.delivery_tag)
            except Exception as e:
                print("FATAL ERROR: WE MISSED A MESSAGE FROM ", self._queue, " ", json.loads(body))
                print(e)
                pass

    def run(self):
        import collections
        collections.Callable = collections.abc.Callable

        rabbit_credential = pika.PlainCredentials(
            settings.BOTON_RABBIT_USERNAME,
            settings.BOTON_RABBIT_PASSWORD
        )
        rabbit_parameters = pika.ConnectionParameters(
            settings.BOTON_HOST,
            settings.BOTON_PORT,
            settings.BOTON_RABBIT_VHOST,
            rabbit_credential
        )
        rabbit_connection = pika.BlockingConnection(rabbit_parameters)
        channel = rabbit_connection.channel()

        print(self._queue, '\n')

        channel.queue_declare(queue=self._queue, durable=True, )

        channel.basic_consume(
            self.callback_func,
            self._queue,
            no_ack=False,
        )

        channel.start_consuming()
