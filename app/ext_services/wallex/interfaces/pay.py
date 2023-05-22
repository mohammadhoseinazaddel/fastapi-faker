import requests

from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.config import settings
from ..exceptions.oauth import WallexError
from ..exceptions.pay import WallexErrorCode1000, WallexErrorCode1001, WallexErrorCode1002, WallexErrorCode1003, \
    WallexErrorCode1004, WallexPayUndefinedError, WallexPay422Error
from ..models.pay_in_wallex import wallex_pay_crud
from ..models.schemas.pay_in_wallex import CreateWallexPay, UpdateWallexPay, GetMultiWallexPay


class WallexPayInterface(InterfaceBase):

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = wallex_pay_crud
        self.base_wallex_url = settings.WALLEX_API_BASE_UERL
        self.wallex_pay_api_key = settings.WALLEX_PAY_API_KEY

        self.STATUS_CREATED = 'CREATED'
        self.STATUS_UNVERIFIED = 'UNVERIFIED'
        self.STATUS_CONFIRMED = 'CONFIRMED'
        self.STATUS_REJECTED_BY_USER = 'REJECTED_BY_USER'
        self.STATUS_REJECTED_BY_SYSTEM = 'REJECTED_BY_SYSTEM'

    def api_create_request(
            self,
            assets: list,
            user_id: int,
            order_id: str,
            state: str,
            callback_url: str,
    ):
        url = settings.WALLEX_API_BASE_UERL + '/v1/wpay/start'
        headers = {
            'x-wpay-api-key': self.wallex_pay_api_key
        }
        json_data = {
            'assets': assets,
            'callback_url': callback_url,
            'user_id': user_id,
            'order_id': str(order_id),
            'state': state,
        }
        try:
            response = requests.post(url, headers=headers, json=json_data)
        except Exception as e:
            raise WallexError

        if response.status_code == 200:
            return response.json()

        else:
            print(response.json())
            self._exception_handler_wallex_pay_request(response=response)

    def api_inquiry_request(
            self,
            token: str,
    ):
        url = settings.WALLEX_API_BASE_UERL + f'/v1/wpay/transaction/{token}'
        headers = {
            'x-wpay-api-key': settings.WALLEX_PAY_API_KEY
        }

        try:
            response = requests.get(url, headers=headers, )
        except Exception as e:
            raise WallexError

        if response.status_code == 200:
            return response.json()

        else:
            self._exception_handler_wallex_pay_request(response=response)

    def api_confirm_request(
            self,
            token: str,
    ):
        url = settings.WALLEX_API_BASE_UERL + f'/v1/wpay/transaction/{token}'
        headers = {
            'x-wpay-api-key': settings.WALLEX_PAY_API_KEY
        }

        json_data = {
            'action': 'confirm'
        }

        try:
            response = requests.post(url, headers=headers, json=json_data)
        except Exception as e:
            raise WallexError

        if response.status_code == 200:
            return response.json()

        else:
            self._exception_handler_wallex_pay_request(response=response)

    def api_reject_request(
            self,
            token: str,
    ):
        url = settings.WALLEX_API_BASE_UERL + f'/v1/wpay/transaction/{token}'
        headers = {
            'x-wpay-api-key': settings.WALLEX_PAY_API_KEY
        }

        json_data = {
            'action': 'reject'
        }

        try:
            response = requests.post(url, headers=headers, json=json_data)
        except Exception as e:
            raise WallexError

        if response.status_code == 200:
            return response.json()

        else:
            self._exception_handler_wallex_pay_request(response=response)

    def _exception_handler_wallex_pay_request(self, response):
        if response.status_code == 500:
            raise WallexErrorCode1000

        elif response.status_code == 404:
            raise WallexErrorCode1001

        elif response.status_code == 403:
            raise WallexErrorCode1002

        elif response.status_code == 400:
            if response.json()['result']['error_code'] == 1003:
                raise WallexErrorCode1003

            elif response.json()['result']['error_code'] == 1004:
                raise WallexErrorCode1004

        elif response.status_code == 422:
            raise WallexPay422Error

        else:
            raise WallexPayUndefinedError


wallex_pay_agent = WallexPayInterface(
    crud=wallex_pay_crud,
    create_schema=CreateWallexPay,
    update_schema=UpdateWallexPay,
    get_multi_schema=GetMultiWallexPay
)
