import json

import pika
import requests
from ext_services.boton.exceptions.boton import (
    WallexBotonAddressManagementError, WallexBotonAddressVerifiactionError)
from system.config import settings


class BotonInterface(object):

    def __init__(self):
        # self.channel = None
        self.rabbit_credential = pika.PlainCredentials(
            settings.BOTON_RABBIT_USERNAME,
            settings.BOTON_RABBIT_PASSWORD
        )
        self.rabbit_parameters = pika.ConnectionParameters(
            settings.BOTON_HOST,
            settings.BOTON_PORT,
            f'/api/vhosts/{settings.BOTON_RABBIT_VHOST}',
            self.rabbit_credential
        )
        # self.rabbit_connection = pika.BlockingConnection(self.rabbit_parameters)

    # address
    @staticmethod
    def get_address_from_blockchain(
            network: str,  # ERC20 | TRC20 | BITCOIN | BITCOIN_CASH | DASH | LITECOIN | DOGECOIN | XLM | EOS | BSC | XRP
            # | BEP2
            user_id: int
    ):
        url = settings.WALLEX_ADDRESS_MANAGEMENT_BASE_URL + f'/api/address/{network}'

        query_params = {
            'userId': user_id
        }

        result = requests.get(
            url=url,
            auth=(
                settings.WALLEX_ADDRESS_MANAGEMENT_USERNAME,
                settings.WALLEX_ADDRESS_MANAGEMENT_PASSWORD
            ),
            params=query_params,
            verify=False,
        )

        if result.status_code == 200:
            return result.json()

        else:
            raise WallexBotonAddressManagementError

    @staticmethod
    def validate_address(
            network: str,
            address: str,
            memo: str
    ):
        url = settings.WALLEX_ADDRESS_MANAGEMENT_BASE_URL + '/api/validate'

        json_data = {
            'network': network,
            'address': address,
            'memo': memo
        }

        result = requests.post(
            url=url,
            auth=(
                settings.WALLEX_ADDRESS_MANAGEMENT_USERNAME,
                settings.WALLEX_ADDRESS_MANAGEMENT_PASSWORD
            ),
            json=json_data,
            verify=False,
        )

        if result.status_code == 200:
            return result.json()

        else:
            raise WallexBotonAddressVerifiactionError

    @staticmethod
    def submit_withdraw(
            unique_id: int,
            network: str,
            address: str,
            amount: float,
            coin: str,
            memo: str = None
    ):
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
        queue_name = 'alpha_HNT_' + network
        channel.queue_declare(queue=queue_name, durable=True)

        prop = pika.BasicProperties(
            content_type='application/json',
            content_encoding='utf-8',
            delivery_mode=2,
        )

        json_body = {
            'uniqueId': unique_id,
            'address': address,
            'amount': amount,
            'coin': coin,
            'memo': memo
        }

        res = channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=prop,
            body=json.dumps(json_body),

        )
        rabbit_connection.close()

        return res


boton_agent = BotonInterface
