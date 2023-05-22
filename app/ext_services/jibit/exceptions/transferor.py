from fastapi import status
from system.base.exceptions import Error


class JibitTransferorConnectionError(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit Transferor Connection Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطا در ارتباط با سرویس تسویه حساب (پرداخت) جیبیت',
                'field': '',
                'type': 'Jibit.Transferor.Connection'
            }
        )


class JibitTransferorCredentialError(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit Transferor Credential Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای احراز هویت سرویس پرداخت جیبیت',
                'field': '',
                'type': 'Jibit.Transferor.Credential'
            }
        )


class JibitTransferorServerError(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit Transferor Server Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای داخلی سرویس پرداخت جیبیت',
                'field': '',
                'type': 'Jibit.Transferor.Server'
            }
        )


class JibitTransferorUndefinedError(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit Transferor Undefined Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای سرویس پرداخت جیبیت- خطای تعریف نشده',
                'field': '',
                'type': 'Jibit.Transferor.Undefined'
            }
        )
