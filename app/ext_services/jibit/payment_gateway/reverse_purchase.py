import requests
from system.config import settings
from ext_services.jibit.exceptions.payment_gateway import *


def jibit_pay_gw_reverse_purchase(
        client_ref_num: str,
        purchase_id: int,
):
    headers = {
        'Authorization': 'Bearer ' + settings.JIBIT_PAY_GW_ACCESS_TOKEN
    }

    json_data = {
        'clientReferenceNumber': client_ref_num,
        'purchaseId': purchase_id,
    }

    try:
        response = requests.post(settings.JIBIT_PAY_GW_BASE_URL + f'/v3/purchases/reverse', headers=headers, json=json_data)
    except Exception as e:
        raise JibitPGConnectionError

    response = response.json()
    """
    Jibit Defined Errors based on their doc :

    purchase.not_found: When the purchase is not found.

    reverse.not_supported: When the refund is not supported for this type of purchase.

    purchase.invalid_state: When the purchase is not in valid (FINISHED) state.

    clientReferenceNumber_or_purchaseId.are_required: When clientReferenceNumber and purchaseId are not provided.

    purchase.not_reversible: When the purchase is not reversible because of internal verification procedures.

    purchase.refunded: When the refund API has called for this purchase; so you can’t reverse it.

    purchase.already_reversed: When the purchase is already reversed.

    ip.not_trusted: When the client IP is not trusted. Read More.

    security.auth_required: The bearer JWT token is not present in request header as the Authorization parameter.
    Read More.

    token.verification_failed: The access token is invalid or expired. Read More.

    web.invalid_or_missing_body: When the request body is not a valid JSON. Read More.

    server.error: Internal server error. Please tell us the value of fingerprint to be able to track the exact problem internally.
    """

    if 'errors' in response:
        for item in response['errors']:
            if item['code'] == 'purchase.not_found':
                raise JibitPgPurchaseNotFound

            elif item['code'] in [
                'reverse.not_supported',
            ]:
                raise JibitPgReverseNotSupported

            elif item['code'] in [
                'purchase.not_reversible',
            ]:
                raise JibitPgNotReversible

            elif item['code'] in [
                'purchase.refunded',
            ]:
                raise JibitPgPurchaseRefunded

            elif item['code'] in [
                'purchase.already_reversed',
            ]:
                raise JibitPgPurchaseAlreadyReversed

            elif item['code'] in [
                'purchase.invalid_state',
            ]:
                raise JibitPgPurchaseIsInInvalidState

            elif item['code'] in [
                'clientReferenceNumber_or_purchaseId.are_required',
                'ip.not_trusted',
                'web.invalid_or_missing_body',
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
        "reverse_status": response['status'] if 'status' in response else None,
    }
    return res
