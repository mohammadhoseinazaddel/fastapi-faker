from starlette import status

from system.base.exceptions import Error


class FinnotechChequeBargashtiError(Error):
    def __init__(self, message=None, error_code=None):
        super().__init__(
            message="Finnotech Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای فینوتک- سرویس چک برگشتی',
                'field': error_code,
                'type': message
            }
        )


class FinnotechChequeCompabilityError(Error):
    def __init__(self, ):
        super().__init__(
            message="Finnotech Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای فینوتک- سرویس چک برگشتی: پیاده سازی سرویس از سمت فینوتک تغییر یافته است',
                'field': '',
                'type': 'Compability'
            }
        )