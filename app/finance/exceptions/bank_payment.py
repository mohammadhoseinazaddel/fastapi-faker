from system.base.exceptions  import Error
from system.config import settings
from fastapi import status


#  CRUD exceptions
class BankPaymentNotFound(Error):
    def __init__(self, ):
        super().__init__(
            message="Bank Payment not found.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'درخواست پرداخت وجود ندارد',
                'field': '',
                'type': ''
            }
        )


class BankPaymentInvalidSummuation(Error):
    def __init__(self, ):
        super().__init__(
            message="Bank Payment Details amounts sum is inconsistent with total amount.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'جمع جزییات درخواست پرداخت با مقدار کل پرداخت مطابقت ندارد.',
                'field': '',
                'type': ''
            }
        )


class BankPaymentMaxAmountExceeded(Error):
    def __init__(self, ):
        super().__init__(
            message="Bank Payment Max Amount Exceeded",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': f'مبلغ پرداختی نمی تواند از {settings.MAXIMUM_BANK_PAYMENT_AMOUNT} بیش تر باشد.',
                'field': 'amount',
                'type': 'Bank.Payment.Max.Amount.Exceeded'
            }
        )


class BankPaymentMinAmountError(Error):
    def __init__(self, ):
        super().__init__(
            message="Bank Payment Minimum Amount Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': f'مبلغ پرداخت باید از {settings.MINIMUM_BANK_PAYMENT_AMOUNT} بیشتر باشد ',
                'field': 'amount',
                'type': 'Bank.Payment.Minimum.Amount.Error'
            }
        )


class BankPaymentHasAnUnfinishedPaymentGateway(Error):
    def __init__(self, ):
        super().__init__(
            message="Bank Payment Has An Unfinished Payment Gateway",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'درخواست پرداخت مورد نظر به درگاه ارسال شده و هنوز پاسخی دریافت نشده است. لطفا تا مشخص شدن نتیجه صبوری کنید',
                'field': '',
                'type': 'Bank.Payment.Has.An.Unfinished.Payment.Gateway'
            }
        )


class BankPaymentPaid(Error):
    def __init__(self, ):
        super().__init__(
            message="Bank Payment Paid",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'درخواست پرداختت مورد نظر پیش از این پرداخت شده است.',
                'field': '',
                'type': 'Bank.Payment.Paid'
            }
        )