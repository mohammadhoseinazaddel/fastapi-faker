import json
import requests
from system.config import settings
from ext_services.jibit.exceptions.transferor import JibitTransferorConnectionError, JibitTransferorCredentialError, \
    JibitTransferorServerError, JibitTransferorUndefinedError


def jibit_transferor_get_token():
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'apiKey': settings.JIBIT_TRANSFEROR_API_KEY,
        'secretKey': settings.JIBIT_TRANSFEROR_SECRET_KEY,
    }

    try:
        response = requests.post(settings.JIBIT_TRANSFEROR_BASE_URL + '/v2/tokens/generate', headers=headers, json=json_data)
    except Exception as e:
        raise JibitTransferorConnectionError

    response = response.json()

    ''' Possible errors based on jibit document
        'invalid.request_body',
        'apiKey.is_required',
        'apiKey.invalid_length',
        'secretKey.is_required',
        'secretKey.invalid_length',
        'invalid.credentials',
        'server.error',
    '''

    if 'errors' in response:
        for item in response['errors']:
            if item['code'] in [
                'invalid.request_body',
                'apiKey.is_required',
                'apiKey.invalid_length',
                'secretKey.is_required',
                'secretKey.invalid_length',
                'invalid.credentials',
            ]:
                raise JibitTransferorCredentialError

            elif item['code'] == 'server.error':
                raise JibitTransferorServerError

            else:
                raise JibitTransferorUndefinedError

    if 'accessToken' in response:
        settings.JIBIT_TRANSFEROR_ACCESS_TOKEN = response['accessToken']

    if 'refreshToken' in response:
        settings.JIBIT_TRANSFEROR_REFRESH_TOKEN = response['refreshToken']

    else:
        raise JibitTransferorUndefinedError

    return response


def jibit_transferor_get_refresh_token():
    headers = {
        # 'accept': 'application/json',
        # Already added when you pass json= but not when you pass data=
        'Content-Type': 'application/json',
    }

    json_data = {
        'accessToken': settings.JIBIT_TRANSFEROR_ACCESS_TOKEN,
        'refreshToken': settings.JIBIT_TRANSFEROR_REFRESH_TOKEN,
    }
    try:
        response = requests.post(settings.JIBIT_TRANSFEROR_BASE_URL + '/v2/tokens/refresh', headers=headers, json=json_data)
    except Exception as e:
        raise JibitTransferorConnectionError

    response = response.json()

    ''' Possible errors based on jibit document
        'invalid.request_body',
        'accessToken.is_required',
        'refreshToken.is_required',
        'refreshToken.not_valid',
        'invalid.tokens_pair',
        'client.not_found',
        'server.error'
    '''

    if 'errors' in response:
        for item in response['errors']:
            if item['code'] == 'refreshToken.not_valid':
                jibit_transferor_get_token()
                json_data = {
                    'accessToken': settings.JIBIT_TRANSFEROR_ACCESS_TOKEN,
                    'refreshToken': settings.JIBIT_TRANSFEROR_REFRESH_TOKEN,
                }
                try:
                    response = requests.post(settings.JIBIT_TRANSFEROR_BASE_URL + '/v2/tokens/refresh', headers=headers,
                                             json=json_data)
                except Exception as e:
                    raise JibitTransferorConnectionError

                response = response.json()
                if 'errors' in response:
                    for item in response['errors']:
                        if item['code'] in [
                            'invalid.request_body',
                            'accessToken.is_required',
                            'refreshToken.is_required',
                            'refreshToken.not_valid',
                            'invalid.tokens_pair',
                            'client.not_found',
                        ]:
                            raise JibitTransferorCredentialError

            if item['code'] in [
                            'invalid.request_body',
                            'accessToken.is_required',
                            'refreshToken.is_required',
                            'refreshToken.not_valid',
                            'invalid.tokens_pair',
                            'client.not_found',
                        ]:
                raise JibitTransferorCredentialError

            elif item['code'] in ['server.error']:
                raise JibitTransferorServerError
            else:
                raise JibitTransferorUndefinedError

    if 'refreshToken' and 'accessToken' in response:
        settings.JIBIT_TRANSFEROR_ACCESS_TOKEN = response['accessToken']
        settings.JIBIT_TRANSFEROR_REFRESH_TOKEN = response['refreshToken']

    return response

