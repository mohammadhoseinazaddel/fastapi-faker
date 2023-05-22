import datetime
import requests
from system.config import settings
from ext_services.jibit.exceptions.payment_gateway import *
from ext_services.jibit.payment_gateway.schema.payment_gateway_inquiry import PaymentGatewayInquiry
from ext_services.jibit.payment_gateway.schema.payment_gateway_inquiry_result import PaymentGatewayInquiryResult


def jibit_pay_gw_inquiry_purchase(
        client_ref_num: str = None,
        from_date: datetime = None,
        to_date: datetime = None,
        page: int = 0,
        psp_ref_num: str = None,
        psp_rrn: str = None,
        psp_trace_num: str = None,
        purchase_id: str = None,
        size: int = 0,
        pgp_status: str = None,
        user_identifier: str = None,
) -> PaymentGatewayInquiryResult:
    headers = {
        'Authorization': 'Bearer ' + settings.JIBIT_PAY_GW_ACCESS_TOKEN
    }

    query_params = {
        'clientReferenceNumber': client_ref_num,
        'from': from_date,
        'page': page,
        'pspReferenceNumber': psp_ref_num,
        'pspRrn': psp_rrn,
        'pspTraceNumber': psp_trace_num,
        'size': size,
        'status': pgp_status,
        'to': to_date,
        'userIdentifier': user_identifier,
        'purchaseId': purchase_id,
    }

    url = settings.JIBIT_PAY_GW_BASE_URL + '/v3/purchases'

    try:
        response = requests.get(url, params=query_params, headers=headers)
    except Exception as e:
        raise JibitPGConnectionError

    response = response.json()

    """
    Jibit Define Error Should Be Handel :
        'page_number.max_exceeded',
        'page_size.max_exceeded',
        'ip.not_trusted',
        'client.not_active',
        'security.auth_required',
        'token.verification_failed',
        'web.invalid_or_missing_body',
        'server.error'
    """

    if 'errors' in response:
        for item in response['errors']:
            if item['code'] == 'page_number.max_exceeded':
                raise JibitPgPageNumMaxExceeded

            if item['code'] == 'page_size.max_exceeded':
                raise JibitPgPageSizeMaxExceeded

            if item['code'] in [
                'ip.not_trusted',
                'client.not_active',
                'security.auth_required',
                'token.verification_failed',
                'web.invalid_or_missing_body',
            ]:
                raise JibitPgWallpayCompabilityError(jibit_message=item['code'])

            elif item['code'] == 'server.error':
                raise JibitPGServerError
            else:
                raise JibitPGUndefinedError
    li = []
    if 'elements' in response:
        for item in response['elements']:
            add_item = PaymentGatewayInquiry(
                purchase_id=item['purchaseId'] if 'purchaseId' in item else 0,
                amount=item['amount'] if 'amount' in item else None,
                wage=item['wage'] if 'wage' in item else None,
                fee=item['fee'] if 'fee' in item else None,
                fee_payment_type=item['feePaymentType'] if 'feePaymentType' in item else None,
                currency=item['currency'] if 'currency' in item else None,
                callback_url=item['callbackUrl'] if 'callbackUrl' in item else None,
                psp_status=item['state'] if 'state' in item else None,
                client_ref_num=item['clientReferenceNumber'] if 'clientReferenceNumber' in item else None,
                psp_name=item['pspName'] if 'pspName' in item else None,
                psp_rrn=item['pspRrn'] if 'pspRrn' in item else None,
                psp_ref_num=item['pspReferenceNumber'] if 'pspReferenceNumber' in item else None,
                psp_trace_num=item['pspTraceNumber'] if 'pspTraceNumber' in item else None,
                expire_date=item['expirationDate'] if 'expirationDate' in item else None,
                user_identifier=item['userIdentifier'] if 'userIdentifier' in item else None,
                payer_mobile_num=item['payerMobileNumber'] if 'payerMobileNumber' in item else None,
                addition_date=item['additionalData'] if 'additionalData' in item else None,
                psp_masked_card_num=item['pspMaskedCardNumber'] if 'pspMaskedCardNumber' in item else None,
                payer_ip=item['initPayerIp'] if 'initPayerIp' in item else None,
                redirect_payer_ip=item['redirectPayerIp'] if 'redirectPayerIp' in item else None,
                psp_settled=item['pspSettled'] if 'pspSettled' in item else None,
                created_at=item['createdAt'] if 'createdAt' in item else None,
                billing_date=item['billingDate'] if 'billingDate' in item else None,
                verified_at=item['verifiedAt'] if 'verifiedAt' in item else None,
                psp_settled_at=item['pspSettledAt'] if 'pspSettledAt' in item else None
            )
            li.append(add_item)

    return PaymentGatewayInquiryResult(
        page_number=response['pageNumber'] if 'pageNumber' in response else None,
        size=response['size'] if 'size' in response else None,
        number_of_elements=response['numberOfElements'] if 'numberOfElements' in response else None,
        has_next=response['hasNext'] if 'hasNext' in response else None,
        has_previous=response['hasPrevious'] if 'hasPrevious' in response else None,
        purchases=li
    )
