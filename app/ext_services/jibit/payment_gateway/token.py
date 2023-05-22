import json
import requests
from system.config import settings
from ext_services.jibit.exceptions.payment_gateway import JibitPGConnectionError, JibitPGCredentialError, \
    JibitPGServerError, JibitPGUndefinedError


def jibit_pay_gw_get_token():
    headers = {
        'accept': 'application/json',
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'apiKey': settings.JIBIT_PAY_GW_API_KEY,
        'secretKey': settings.JIBIT_PAY_GW_SECRET_KEY,
    }

    try:
        response = requests.post(settings.JIBIT_PAY_GW_BASE_URL + '/v3/tokens', headers=headers, json=json_data)
    except Exception as e:
        raise JibitPGConnectionError

    response = response.json()
    defined_errors = [
        'security.bad_credentials',
        'client.not_active',
        'apiKey.is_required',
        'secretKey.is_required',
        'web.invalid_or_missing_body',
        'server.error',
    ]
    if 'errors' in response:
        for item in response['errors']:
            if item['code'] in defined_errors[0:5]:
                raise JibitPGCredentialError
            elif item['code'] == defined_errors[5]:
                raise JibitPGServerError
            else:
                raise JibitPGUndefinedError

    if 'accessToken' in response:
        settings.JIBIT_PAY_GW_ACCESS_TOKEN = response['accessToken']

    if 'refreshToken' in response:
        settings.JIBIT_PAY_GW_REFRESH_TOKEN = response['refreshToken']

    else:
        raise JibitPGUndefinedError

    return response


def jibit_pay_gw_get_refresh_token():
    headers = {
        'accept': 'application/json',
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'refreshToken': settings.JIBIT_PAY_GW_REFRESH_TOKEN,
    }
    try:
        response = requests.post(settings.JIBIT_PAY_GW_BASE_URL + '/v3/tokens/refresh', headers=headers, json=json_data)
    except Exception as e:
        raise JibitPGConnectionError

    response = response.json()
    defined_errors = [
        'security.bad_credentials',
        'client.not_active',
        'refreshToken.is_required',
        'web.invalid_or_missing_body',
        'server.error',
    ]

    if 'errors' in response:
        for item in response['errors']:
            if item['code'] == defined_errors[0]:
                jibit_pay_gw_get_token()
                json_data = {
                    'refreshToken': 'string',
                }
                try:
                    response = requests.post(settings.JIBIT_PAY_GW_BASE_URL + '/v3/tokens/refresh', headers=headers,
                                             json=json_data)
                except Exception as e:
                    raise JibitPGConnectionError

                response = response.json()
                if 'errors' in response:
                    for item in response['errors']:
                        if item['code'] == defined_errors[0]:
                            raise JibitPGCredentialError

            elif item['code'] in defined_errors[1:3]:
                raise JibitPGCredentialError

            elif item['code'] in defined_errors[5:]:
                raise JibitPGServerError
            else:
                raise JibitPGUndefinedError

    if 'refreshToken' and 'accessToken' in response:
        settings.JIBIT_PAY_GW_ACCESS_TOKEN = response['accessToken']
        settings.JIBIT_PAY_GW_REFRESH_TOKEN = response['refreshToken']

    return response

