from system.base.exceptions import Error
from fastapi import status


#  CRUD exceptions
class UserAlreadyHaveBankProfile(Error):
    def __init__(self, ):
        super().__init__(
            message="User already have bank profile",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'در حال حاضر پروفایل بانکی برای شما وجود دارد.',
                'field': '',
                'type': ''
            }
        )


class UserNotVerified(Error):
    def __init__(self, ):
        super().__init__(
            message="User not verified",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'کاربر هنوز اهراز هویت نشده است.',
                'field': '',
                'type': 'system-error'
            }
        )
