# define Python user-defined exceptions
from fastapi import status


class Error(Exception):
    """Base class for other exceptions"""

    def __init__(self, message="", errors=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        if errors is None:
            errors = {}
        self.errors = errors


class UnExpectedError(Error):
    def __init__(self, ):
        super().__init__(
            message="User not found.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'UnExpected Error',
                'field': '',
                'type': 'UnExpected Error'
            }
        )


class HTTP_401_Walpay(Error):
    def __init__(self, ):
        super().__init__(
            message="UnAuthorized",
            errors={
                'code': status.HTTP_401_UNAUTHORIZED,
                'message': 'خطا در احراز هویت',
                'type': 'UnAuthorized'
            }
        )


class HTTP_401_Otp_Walpay(Error):
    def __init__(self, ):
        super().__init__(
            message="UnAuthorized",
            errors={
                'code': status.HTTP_401_UNAUTHORIZED,
                'message': 'کد وارد شده نامعتبر است',
                'type': 'UnAuthorized'
            }
        )


class HTTP_500_Walpay(Error):
    def __init__(self, ):
        super().__init__(
            message="UnAuthorized",
            errors={
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'خطای داخلی سرور',
                'field': '',
                'type': 'Internal.Server.Error'
            }
        )


class GetMultiSchemNotDefined(Error):
    def __init__(self):
        super().__init__(
            message="Get-multi-schema not defined",
            errors={
                'code': 500,
                'message': '',
            }
        )
