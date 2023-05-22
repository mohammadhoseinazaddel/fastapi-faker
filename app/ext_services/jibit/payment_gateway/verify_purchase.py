import requests
from system.config import settings
from ext_services.jibit.exceptions.payment_gateway import *


def jibit_pay_gw_verify_purchase(
        purchase_id: int,
):
    headers = {
        'Authorization': 'Bearer ' + settings.JIBIT_PAY_GW_ACCESS_TOKEN
    }

    json_data = {
        'purchaseId': purchase_id,
    }

    try:
        response = requests.post(settings.JIBIT_PAY_GW_BASE_URL + f'/v3/purchases/{purchase_id}/verify', headers=headers, json=json_data)
    except Exception as e:
        raise JibitPGConnectionError

    response = response.json()
    """
    Jibit Define Error Should Be Handel :
        'ip.not_trusted',
        'client.not_active',
        'purchase.not_found',
        'security.auth_required',
        'token.verification_failed',
        'server.error'
    """

    if 'errors' in response:
        for item in response['errors']:
            if item['code'] == 'purchase.not_found':
                raise JibitPGAmountNotEnough

            if item['code'] in [
                'ip.not_trusted',
                'client.not_active',
                'security.auth_required',
                'token.verification_failed',
            ]:
                raise JibitPgWallpayCompabilityError(jibit_message=item['code'])

            elif item['code'] == 'server.error':
                raise JibitPGServerError
            else:
                raise JibitPGUndefinedError

    res = {
        "errors": [item['code'] for item in response['errors']] if 'errors' in response else [],
        "psp_status": response['status'] if 'status' in response else None,
    }
    return res
