from system.base.exceptions  import Error
from fastapi import status


class JibitPGConnectionError(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit PG Connection Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'Jibit PG Connection Error',
                'type': 'Jibit.PG.Connection'
            }
        )


class JibitPGCredentialError(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit PG Credential Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'Jibit PG Credential Error',
                'type': 'Jibit.PG.Credential'
            }
        )


class JibitPGAmountNotEnough(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit PG Amount Not Enough",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه: مقدار پرداخت کافی (مجاز) نیست',
                'type': 'Jibit.PG.Amount.Not.Enough'
            }
        )


class JibitPGServerError(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit PG Server Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه پرداخت- لطفا مجددا تلاش فرمایید',
                'field': '',
                'type': 'Jibit.PG.Server'
            }
        )


class JibitPGUndefinedError(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit PG Undefined Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه پرداخت- خطای تعریف نشده',
                'field': '',
                'type': 'Jibit.PG.Undefined'
            }
        )


class JibitPgWageInvalid(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit PG Wage Invalid",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه پرداخت: کارمزد نامعتبر',
                'field': '',
                'type': 'Jibit.PG.Wage.Invalid'
            }
        )


class JibitPgAmountMaxExceeded(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit PG Amount+Wage Max Exceeded",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه پرداخت: مبلغ بیش از سقف مجاز',
                'field': '',
                'type': 'Jibit.PG.Amount+Wage.Max.Exceeded'
            }
        )


class JibitPgClientReferenceNumberDuplicated(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit PG Client Reference Number Duplicated",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه پرداخت: درخواست پرداخت پیش از این ارسال شده است',
                'field': '',
                'type': 'Jibit.PG.ClientReferenceNumber.Duplicated'
            }
        )


class JibitPgWallpayCompabilityError(Error):
    def __init__(self, jibit_message=None):
        super().__init__(
            message="Jibit PG Wallpay Compability Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه پرداخت: خطای پیش بینی نشده لطفا با پشتیبانی وال پی تماس بگیرید',
                'field': '',
                'type': jibit_message
            }
        )


class JibitPgPurchaseNotFound(Error):
    def __init__(self, jibit_message=None):
        super().__init__(
            message="Jibit PG Purchase Not Found",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه پرداخت: درخواست پرداخت مورد نظر یافت نشد',
                'field': '',
                'type': 'purchase.not_found'
            }
        )


class JibitPgPageNumMaxExceeded(Error):
    def __init__(self, jibit_message=None):
        super().__init__(
            message="Jibit PG Page Number Max Exceeded",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه پرداخت: شماره صفحه از حد مجاز بیشتر است',
                'field': '',
                'type': 'page_number.max_exceeded'
            }
        )


class JibitPgPageSizeMaxExceeded(Error):
    def __init__(self, jibit_message=None):
        super().__init__(
            message="Jibit PG Page Size Max Exceeded",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه پرداخت: تعداد رکوردهای صفحه از حد مجاز بیشتر است',
                'field': '',
                'type': 'page_size.max_exceeded'
            }
        )


class JibitPgReverseNotSupported(Error):
    def __init__(self, jibit_message=None):
        super().__init__(
            message="Jibit PG Reverse Not Supported",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه جیبیت: ریوریس برای ابن نوع پرداخت پشتیبانی نمی شود.',
                'field': '',
                'type': 'reverse.not.supported'
            }
        )


class JibitPgNotReversible(Error):
    def __init__(self, jibit_message=None):
        super().__init__(
            message="Jibit PG Not Reversible",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه جیبیت: این نوع پرداخت غیر قابل ریورس است',
                'field': '',
                'type': 'not.reversible'
            }
        )


class JibitPgPurchaseRefunded(Error):
    def __init__(self, jibit_message=None):
        super().__init__(
            message="Jibit PG Purchase Refunded",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه جیبیت: پرداخت قبلا ریفاند شده است',
                'field': '',
                'type': 'purchase.refunded'
            }
        )


class JibitPgPurchaseAlreadyReversed(Error):
    def __init__(self, jibit_message=None):
        super().__init__(
            message="Jibit PG Purchase Already Reversed",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه جیبیت: پرداخت قبلا با موفقیت ریورس شد است',
                'field': '',
                'type': 'purchase.already.reversed'
            }
        )


class JibitPgPurchaseIsInInvalidState(Error):
    def __init__(self, jibit_message=None):
        super().__init__(
            message="Jibit PG Purchase Is In Invalid Reversed",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای درگاه جیبیت: پرداخت در وضعیت finished قرار نداشته و قابل ریورس نبود',
                'field': '',
                'type': 'purchase.is.in.invalid.state'
            }
        )
