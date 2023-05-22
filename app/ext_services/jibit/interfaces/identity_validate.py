import json
from datetime import date

import jdatetime
import requests

from ext_services.jibit.exceptions.identity_validate import JibitConnectionError, JibitCredentialError, \
    JibitServerError, JibitUndefinedError, JibitUnexpectedErrorInput
from system.config import settings
from system.logger.log import ext_service_logger


class JibitIdentityValidate:

    @staticmethod
    def jibit_get_token():
        url = settings.JIBIT_IDEN_VALID_BASE_URL + '/v1/tokens/generate'
        payload = {
            'apiKey': settings.JIBIT_IDEN_VALID_API_KEY,
            'secretKey': settings.JIBIT_IDEN_VALID_SECRET_KEY
        }
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)
        except Exception as e:
            raise JibitConnectionError

        response = response.json()
        defined_errors = [
            'invalid.request_body',
            'apiKey.is_required',
            'apiKey.length_exceeded',
            'secretKey.is_required',
            'secretKey.length_exceeded',
            'invalid.credentials',
            'server.error'
        ]
        if 'code' in response:
            if response['code'] in defined_errors[0:6]:
                raise JibitCredentialError
            elif response['code'] == defined_errors[6]:
                raise JibitServerError
            else:
                raise JibitUndefinedError

        if 'accessToken' in response:
            settings.JIBIT_IDEN_VALID_ACCESS_TOKEN = response['accessToken']

        if 'refreshToken' in response:
            settings.JIBIT_IDEN_VALID_REFRESH_TOKEN = response['refreshToken']

        else:
            raise JibitUndefinedError

        return response

    def jibit_get_refresh_token(self):
        url = settings.JIBIT_IDEN_VALID_BASE_URL + '/v1/tokens/refresh'
        payload = {
            'accessToken': settings.JIBIT_IDEN_VALID_ACCESS_TOKEN,
            'refreshToken': settings.JIBIT_IDEN_VALID_REFRESH_TOKEN
        }
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)
        except Exception as e:
            raise JibitConnectionError

        response = response.json()
        defined_errors = [
            'invalid.request_body',
            'accessToken.is_required',
            'refreshToken.is_required',
            'refreshToken.not_valid',
            'invalid.token_pairs',
            'client.not_found',
            'server.error',
        ]

        if 'code' in response:
            if response['code'] in defined_errors[2:4]:
                self.jibit_get_token()
                payload = {
                    'accessToken': settings.JIBIT_IDEN_VALID_ACCESS_TOKEN,
                    'refreshToken': settings.JIBIT_IDEN_VALID_REFRESH_TOKEN
                }
                try:
                    response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)
                except Exception as e:
                    raise JibitConnectionError

                response = response.json()
                if 'code' in response:
                    if response['code'] in defined_errors[2:4]:
                        raise JibitUndefinedError

            elif response['code'] in defined_errors[0:3]:
                raise JibitUnexpectedErrorInput

            elif response['code'] in defined_errors[5:]:
                raise JibitServerError
            else:
                raise JibitUndefinedError

        if 'refreshToken' and 'accessToken' in response:
            settings.JIBIT_IDEN_VALID_ACCESS_TOKEN = response['accessToken']
            settings.JIBIT_IDEN_VALID_REFRESH_TOKEN = response['refreshToken']

        return response

    def jibit_get_identity(
            self,
            national_code: str,
            birth_date: str
    ):
        query_string = '?nationalCode=' + national_code + '&birthDate=' + birth_date
        url = settings.JIBIT_IDEN_VALID_BASE_URL + '/v1/services/identity' + query_string
        headers = {
            'Authorization': 'Bearer ' + settings.JIBIT_IDEN_VALID_ACCESS_TOKEN
        }
        try:
            result = {
                "is_valid": False,
                "had_system_error": False,
                "error_message": "",
                "user_info": None
            }
            response = requests.request("GET", url, headers=headers, verify=False)
            ext_service_logger.info(f"Jibit_get_identity({national_code}, {birth_date}) -> {response.text}")
            response = response.json()

            # مشکل توکن
            if 'code' in response and response['code'] == 'forbidden':
                self.jibit_get_token()
                headers = {
                    'Authorization': 'Bearer ' + settings.JIBIT_IDEN_VALID_ACCESS_TOKEN
                }
                response = requests.request("GET", url, headers=headers, verify=False)
                ext_service_logger.info(f"Jibit_get_identity({national_code}, {birth_date}) -> {response.text}")
                response = response.json()

            if 'code' in response and response['code'] in ['forbidden', 'daily_limit.reached',
                                                           'providers.not_available', 'server.error']:
                result['had_system_error'] = True
                return result

            #  اطلاعات غیر معتیر
            if 'code' in response and response['code'] == 'identity_info.not_found':
                result['error_message'] = response['message']
                return result

            # اطلاعات معتبر
            if 'nationalCode' in response:
                user = {
                    "national_code": response['nationalCode'],
                    "persian_birth_date": response["birthDate"],
                    "first_name": response['identityInfo']['firstName'],
                    "last_name": response['identityInfo']['lastName'],
                    "father_name": response['identityInfo']['fatherName'],
                    # "gender": response['identityInfo']['gender'],
                    "is_alive": response['identityInfo']['alive'],
                    # "provider_tracker_id": response['identityInfo']['providerTrackerId'],
                    # "identification_number": response['identityInfo']['identificationNumber'],
                    # "identification_serial_code": response['identityInfo']['identificationSerialCode'],
                    # "identification_serial_number": response['identityInfo']['identificationSerialNumber'],
                    "provider_tracker_id": '0000',
                    "identification_number": '0000',
                    "identification_serial_code": '0000',
                    "identification_serial_number": '0000',
                }
                result['user_info'] = user
                result['is_valid'] = True

                return result

        except Exception as e:
            return {
                "is_valid": False,
                "had_system_error": True,
                "error_message": "API connection or unexpected error",
                "user_info": None
            }
        return result

    # match_national_code_w_mobile
    def jibit_shahkar(
            self,
            national_code: str,
            mobile: str
    ):
        query_string = '?nationalCode=' + national_code + '&mobileNumber=' + str(mobile)
        url = settings.JIBIT_IDEN_VALID_BASE_URL + '/v1/services/matching' + query_string
        headers = {
            'Authorization': 'Bearer ' + settings.JIBIT_IDEN_VALID_ACCESS_TOKEN
        }
        try:
            result = {
                "is_valid": False,
                "had_system_error": False,
                "error_message": "",
            }
            response = requests.request("GET", url, headers=headers, verify=False)
            ext_service_logger.info(f"Jibit_get_identity({national_code}, {mobile}) -> {response.text}")
            response = response.json()

            # مشکل توکن
            if 'code' in response and response['code'] == 'forbidden':
                self.jibit_get_token()
                headers = {
                    'Authorization': 'Bearer ' + settings.JIBIT_IDEN_VALID_ACCESS_TOKEN
                }
                response = requests.request("GET", url, headers=headers, verify=False)
                ext_service_logger.info(f"Jibit_get_identity({national_code}, {mobile}) -> {response.text}")
                response = response.json()

            if 'code' in response and response['code'] in ['forbidden', 'daily_limit.reached',
                                                           'providers.not_available', 'server.error']:
                result['had_system_error'] = True
                return result

            #  اطلاعات غیر معتیر
            if 'matched' in response and not response['matched']:
                result['is_valid'] = False
                return result

            # اطلاعات معتبر
            if 'matched' in response and response['matched']:
                result['is_valid'] = True

                return result

        except Exception as e:
            return {
                "is_valid": False,
                "had_system_error": True,
                "error_message": "API connection or unexpected error",
            }
        return result

    def get_identity(self, national_code: str, georgian_birth_date: date):
        birth_date_persian = str(jdatetime.date.fromgregorian(date=georgian_birth_date)).replace('-', '')
        res = self.jibit_get_identity(national_code, birth_date_persian)
        return res

    def shahkar_validation(self, national_code: str, mobile: str):
        res = self.jibit_shahkar(national_code, mobile)
        return res

    def _request_to_jibit_for_matching_number_with_national_code(
            self,
            birth_date: date,
            card_number: str,
            national_code: str
    ):
        persian_birthdate = str(jdatetime.date.fromgregorian(date=birth_date)).replace('-', '')
        query_str = f'?cardNumber={card_number}&nationalCode={national_code}&birthDate={persian_birthdate}'

        headers = {
            'Authorization': 'Bearer ' + settings.JIBIT_IDEN_VALID_ACCESS_TOKEN
        }

        response = requests.request(
            "GET",
            url=settings.JIBIT_IDEN_VALID_BASE_URL + '/v1/services/matching' + query_str,
            headers=headers,
            verify=False
        )

        # Logging
        ext_service_logger.info(
            f"Jibit_match_card_number_with_national_code({card_number}, {national_code}) -> {response.text}")
        json_response = response.json()

        # Get New Token and repeat this method again
        if 'code' in json_response and json_response['code'] == 'forbidden':
            # get new access token
            self.jibit_get_token()

            return self._request_to_jibit_for_matching_number_with_national_code(
                birth_date=birth_date,
                card_number=card_number,
                national_code=national_code
            )
        return json_response

    def _request_to_jibit_for_converting_card_number_to_iban(
            self,
            card_number: str,
    ):
        headers = {'Authorization': 'Bearer ' + settings.JIBIT_IDEN_VALID_ACCESS_TOKEN}
        url = settings.JIBIT_IDEN_VALID_BASE_URL + '/v1/cards' + f'?number={card_number}&iban=true'

        response = requests.request(
            "GET",
            url=url,
            headers=headers,
            verify=False
        )
        ext_service_logger.info(
            f"Jibit_convert_card_number_2_iban({card_number}, ) -> {response.text}")
        response_json = response.json()

        if 'code' in response_json and response_json['code'] == 'forbidden':
            self.jibit_get_token()
            return self._request_to_jibit_for_converting_card_number_to_iban(
                card_number=card_number
            )
        return response_json

    def is_match_card_number_with_national_code(
            self,
            card_number: str,
            national_code: str,
            birth_date: date
    ):
        try:
            result = {
                "is_valid": False,
                "error_message_fa": "",
            }

            # Request to jibit
            jibit_response = self._request_to_jibit_for_matching_number_with_national_code(
                birth_date=birth_date,
                card_number=card_number,
                national_code=national_code
            )

            # User validation fail
            if 'code' in jibit_response:
                if jibit_response['code'] in ['invalid.request_body', "server_error"]:
                    result['error_message_fa'] = 'سرور جیبیت در دسترس نمی باشد لطفا بعدا تلاش کنید'

                if jibit_response['code'] in [
                    'card.not_valid',
                    "daily_limit.reached",
                    "card.not_active",
                    "card.is_expired",
                    "card.account_number_not_valid",
                    "card.owner_not_authorized",
                    "card.registered_as_lost",
                    "card.registered_as_stolen",
                    "card.source_bank_is_not_active",
                    "card.provider_is_not_active",
                    "card.black_listed",
                    "identity_info.not_found",
                    "matching_unknown",
                    "card.provider_is_not_active",
                    "providers.not_available",
                    "handler.not_found"
                ]:
                    result['error_message_fa'] = jibit_response['message']

            # User validation success
            if 'matched' in jibit_response and jibit_response['matched']:
                result['is_valid'] = True

            # if card is valid but is not for this user jibit don't send us any error message
            if not result['error_message_fa']:
                result['error_message_fa'] = "عدم تطابق کاربر و صاحب حساب"

            # return completed result dictionary
            return result

        except Exception as e:
            raise e

    def convert_card_number_to_iban(
            self,
            card_number: str,
    ):
        try:
            result = {
                "is_valid": False,
                "error_message": None,
                'account_number': None,  # shomare hesab
                'iban': None,
                'bank_name': None
            }

            jibit_response = self._request_to_jibit_for_converting_card_number_to_iban(
                card_number=card_number
            )
            if 'code' in jibit_response:
                result['error_message'] = jibit_response['code']

            if 'ibanInfo' in jibit_response:
                result.update(
                    {
                        'iban': jibit_response['ibanInfo']['iban'],
                        'account_number': jibit_response['ibanInfo']['depositNumber'],
                        'bank_name': jibit_response['ibanInfo']['bank'],
                        'is_valid': True
                    }
                )

            return result

        except Exception as e:
            raise e


jibit_identity_agent = JibitIdentityValidate()
