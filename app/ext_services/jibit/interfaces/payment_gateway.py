import datetime

from ext_services.jibit.payment_gateway.refund_purchase import jibit_pay_gw_refund_purchase
from ext_services.jibit.payment_gateway.reverse_purchase import jibit_pay_gw_reverse_purchase
from system.config import settings
from ext_services.jibit.exceptions.payment_gateway import *
from ext_services.jibit.payment_gateway.create_purchase import jibit_pay_gw_create_purchase
from ext_services.jibit.payment_gateway.inquiry_purchase import jibit_pay_gw_inquiry_purchase
from ext_services.jibit.payment_gateway.verify_purchase import jibit_pay_gw_verify_purchase


class JibitPaymentGatewayInterface:
    @staticmethod
    def create_purchase(
            purchase_ref_num: str,
            amount: int,
            description: str,
            user_identifier: str,
            user_mobile_num: str,
            callback_url: str,
            wage: int = 0,
    ):
        try:
            return jibit_pay_gw_create_purchase(purchase_ref_num, amount, description, user_identifier, user_mobile_num,
                                                callback_url, wage)
        except JibitPGConnectionError:
            raise JibitPGConnectionError

        except JibitPGCredentialError:
            raise JibitPGCredentialError

        except JibitPGServerError:
            raise JibitPGServerError

        except JibitPGUndefinedError:
            raise JibitPGUndefinedError

    @staticmethod
    def verify_purcahse(purchase_id: int):
        try:
            return jibit_pay_gw_verify_purchase(purchase_id)

        except Exception as e:
            raise e

    @staticmethod
    def reverse_purchase(client_ref_num: str, purchase_id: int, ):
        try:
            return jibit_pay_gw_reverse_purchase(client_ref_num=client_ref_num, purchase_id=purchase_id)

        except Exception as e:
            raise e

    @staticmethod
    def refund_purchase(
            client_ref_num: str,
            purchase_id: int,
            amount: int = 0,
            cancellable: bool = False,
    ):
        try:
            return jibit_pay_gw_refund_purchase(
                client_ref_num=client_ref_num,
                purchase_id=purchase_id,
                amount=amount,
                cancellable=cancellable
            )

        except Exception as e:
            raise e

    @staticmethod
    def inquiry_purchase(
            client_ref_num: str,
            from_date: datetime,
            to_date: datetime,
            page: int,
            psp_ref_num: str,
            psp_rrn: str,
            psp_trace_num: str,
            purchase_id: str,
            size: int,
            pgp_status: str,
            user_identifier: str,
    ):
        try:
            return jibit_pay_gw_inquiry_purchase(
                client_ref_num=client_ref_num,
                from_date=from_date,
                to_date=to_date,
                page=page,
                psp_ref_num=psp_ref_num,
                psp_rrn=psp_rrn,
                psp_trace_num=psp_trace_num,
                purchase_id=purchase_id,
                size=size,
                pgp_status=pgp_status,
                user_identifier=user_identifier
            )

        except Exception as e:
            raise e


jibit_payment_gw_agent = JibitPaymentGatewayInterface()
