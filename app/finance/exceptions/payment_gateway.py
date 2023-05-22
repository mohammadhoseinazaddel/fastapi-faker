from system.base.exceptions  import Error
from fastapi import status


#  CRUD exceptions
class PaymentGatewayNotFound(Error):
    def __init__(self, ):
        super().__init__(
            message="Payment Gateway not found.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'رکورد درگاه پرداخت وجود ندارد',
                'field': '',
                'type': 'Payment.Gateway.Not.Found'
            }
        )


class PaymentGatewayNotGetPurchaseId(Error):
    def __init__(self, ):
        super().__init__(
            message="Payment Gateway Has Not Got PurchaseId",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'رکورد درگاه پرداخت هنوز شماره پرداخت از درگاه دریافت نکرده است. لطفا مجددا به درگاه ارسال '
                           'شود',
                'field': '',
                'type': 'Payment.Gateway.Not.Get.Purchase.Id'
            }
        )


class ThisBankPaymentHasAnUncompletePaymentGatewayRecord(Error):
    def __init__(self, ):
        super().__init__(
            message="ThisBankPaymentHasAnUncompletePaymentGatewayRecord",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'این درخواست پرداخت پیش از این به درگاه ارسال شده است. لطفا تا مشخص شدن نتیجه صبور باشید',
                'field': '',
                'type': 'ThisBankPaymentHasAnUncompletePaymentGatewayRecord'
            }
        )


class BankPaymentTypeHasNotImplemented(Error):
    def __init__(self, ):
        super().__init__(
            message="BankPaymentTypeHasNotImplemented",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'این نوع درخواست پرداخت هنوز پیاده سازی نشده است',
                'field': '',
                'type': 'BankPaymentTypeHasNotImplemented'
            }
        )
