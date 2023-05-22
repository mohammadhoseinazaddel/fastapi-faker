from system.base.exceptions import Error
from fastapi import status


class WallexErrorCode1000(Error):
    def __init__(self, ):
        super().__init__(
            message="Wallex Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای داخلی والکس،',
                'field': '',
                'type': 'Wallex.500.Error'
            }
        )


class WallexErrorCode1001(Error):
    def __init__(self, ):
        super().__init__(
            message="Wallex 1001 Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای والکس: تراکنش موجود نیست یا منقضی شده است،',
                'field': '',
                'type': 'Wallex.404.Error'
            }
        )


class WallexErrorCode1002(Error):
    def __init__(self, ):
        super().__init__(
            message="Wallex 1002 Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای والکس: برای انجام عملیات مجاز نیستید',
                'field': '',
                'type': 'Wallex.403.Error'
            }
        )


class WallexErrorCode1003(Error):
    def __init__(self, ):
        super().__init__(
            message="Wallex 1003 Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای والکس: وضعیت تراکنش هنگام تایید یا رد، نامعتبر است',
                'field': '',
                'type': 'Wallex.400.Error'
            }
        )


class WallexErrorCode1004(Error):
    def __init__(self, ):
        super().__init__(
            message="Wallex 1004 Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای والکس: موجودی کاربر کافی نیست',
                'field': '',
                'type': 'Wallex.400.Error'
            }
        )


class WallexPay422Error(Error):
    def __init__(self, ):
        super().__init__(
            message="Wallex Pay 422 Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای والکس: خطای 422',
                'field': '',
                'type': 'Wallex.422.Error'
            }
        )


class WallexPayUndefinedError(Error):
    def __init__(self, ):
        super().__init__(
            message="Wallex Pay Undefined Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای والکس: خطای تعریف نشده',
                'field': '',
                'type': 'Wallex.Undefined.Error'
            }
        )