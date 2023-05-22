import json
import requests
from system.config import settings
from ext_services.jibit.exceptions.payment_gateway import *


def jibit_pay_gw_create_purchase(
        purchase_ref_num: str,
        amount: int,
        description: str,
        user_identifier: str,
        user_mobile_num: str,
        callback_url: str,
        wage: int = 0,
):
    headers = {
        'Authorization': 'Bearer ' + settings.JIBIT_PAY_GW_ACCESS_TOKEN
    }

    json_data = {
        'amount': amount,
        'callbackUrl': callback_url,
        'checkPayerNationalCode': False,
        'clientReferenceNumber': purchase_ref_num,
        'currency': "IRR",
        'description': description,
        'userIdentifier': user_identifier,
        'payerMobileNumber': user_mobile_num,
        'wage': wage,
    }
    try:
        response = requests.post(settings.JIBIT_PAY_GW_BASE_URL + '/v3/purchases', headers=headers, json=json_data)
    except Exception as e:
        raise JibitPGConnectionError

    response = response.json()
    """
    Jibit Define Error Should Be Handel :
        'client.not_active',
        'amount.is_required',
        'amount.not_enough',  # *
        'wage.is_invalid',
        'amount_plus_wage.max_value_exceeded',
        'currency.is_required',
        'callbackUrl.is_required',
        'callbackUrl.is_invalid',
        'callbackUrl.max_length',  # max_length 1024
        'clientReferenceNumber.is_required',
        'clientReferenceNumber.duplicated',
        'payerCardNumber.is_invalid',
        'payerNationalCode.is_invalid',
        'userIdentifier.max_length',
        'payerMobileNumber.is_invalid',
        'payerMobileNumber.in_blacklist',
        'payerNationalCode_and_payerMobileNumber.are_required',
        'description.max_length',  # max_length 256 *
        'ip.not_trusted',
        'security.auth_required',
        'token.verification_failed',
        'web.invalid_or_missing_body',
        'server.error'
    """

    if 'errors' in response:
        for item in response['errors']:
            if item['code'] == 'amount.not_enough':
                raise JibitPGAmountNotEnough

            if item['code'] == 'wage.is_invalid':
                raise JibitPgWageInvalid

            if item['code'] == 'amount_plus_wage.max_value_exceeded':
                raise JibitPgAmountMaxExceeded

            if item['code'] == 'clientReferenceNumber.duplicated':
                raise JibitPgClientReferenceNumberDuplicated

            if item['code'] in [
                'client.not_active',
                'amount.is_required',
                'wage.is_invalid',
                'currency.is_required',
                'callbackUrl.is_required',
                'callbackUrl.is_invalid',
                'callbackUrl.max_length',  # max_length 1024
                'clientReferenceNumber.is_required',
                'payerCardNumber.is_invalid',
                'payerNationalCode.is_invalid',
                'userIdentifier.max_length',
                'payerMobileNumber.is_invalid',
                'payerMobileNumber.in_blacklist',
                'payerNationalCode_and_payerMobileNumber.are_required',
                'description.max_length',  # max_length 256 *
                'ip.not_trusted',
                'security.auth_required',
                'token.verification_failed',
                'web.invalid_or_missing_body',
            ]:
                raise JibitPgWallpayCompabilityError(jibit_message=item['code'])

            elif item['code'] == 'server.error':
                raise JibitPGServerError
            else:
                raise JibitPGUndefinedError

    res = {
        "errors": [item['code'] for item in response['errors']] if 'errors' in response else [],
        "purchase_ref_num": purchase_ref_num,
        "psp_purchase_id": response['purchaseId'] if 'purchaseId' in response else None,
        "psp_switching_url": response['pspSwitchingUrl'] if 'pspSwitchingUrl' in response else None,
    }
    return res
