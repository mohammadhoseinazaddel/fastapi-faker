from fastapi import status

from system.base.exceptions import Error


#  User CRUD exceptions
class UserNotFound(Error):
    def __init__(self, ):
        super().__init__(
            message="User not found.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'User not found.',
                'field': '',
                'type': ''
            }
        )


class UserInaccessible(Error):
    def __init__(self, ):
        super().__init__(
            message="User Inaccessible, Disabled or Deleted.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'کاربر حذف شده یا دسترسی به آن محدود شده است.',
                'field': '',
                'type': ''
            }
        )


class UserVerified(Error):
    def __init__(self, ):
        super().__init__(
            message="User Verified",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'کاربر قبلا تایید شده است',
                'field': '',
                'type': ''
            }
        )


class EmailIsGiven(Error):
    def __init__(self, ):
        super().__init__(
            message="Email is given.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'Email is given.',
                'field': '',
                'type': ''
            }
        )


class UsernameIsGiven(Error):
    def __init__(self, ):
        super().__init__(
            message="Username is given.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'Username is given.',
                'field': '',
                'type': ''
            }
        )


class MobileIsGiven(Error):
    def __init__(self, ):
        super().__init__(
            message="Mobile is given.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'Mobile is given.',
                'field': '',
                'type': ''
            }
        )


class NationalCodeIsGiven(Error):
    def __init__(self, ):
        super().__init__(
            message="National code is given.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'کد ملی شما قبلا با شماره ی دیگری ثبت نام شده است.',
                'field': '',
                'type': ''
            }
        )


class UserCanNotDisabled(Error):
    def __init__(self, ):
        super().__init__(
            message="You can NOT disable this user.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'You can NOT disable this user.',
                'field': '',
                'type': ''
            }
        )


class UserCanNotDeleted(Error):
    def __init__(self, ):
        super().__init__(
            message="You can NOT delete this user.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'You can NOT delete this user.',
                'field': '',
                'type': ''
            }
        )


class InvalidMobileNo(Error):
    def __init__(self, ):
        super().__init__(
            message="Invalid Mobile Number",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'شماره موبایل نامعتبر است',
                'field': '',
                'type': ''
            }
        )


class InvalidNationalCode(Error):
    def __init__(self, ):
        super().__init__(
            message="Invalid National Code",
            errors={
                "code": 422,
                "message": "کد ملی کاربر معتبر نیست",
                "field": "user.national_code",
                "type": "data-error"
            }
        )


class ValidateAccessDenied(Error):
    def __init__(self, ):
        super().__init__(
            message="User info is verified. Can NOT change info",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'User info is verified. Can NOT change info',
                'field': '',
                'type': ''
            }
        )


class IdentityServiceError(Error):
    def __init__(self, ):
        super().__init__(
            message="Identity Service Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'Identity Service Error',
                'field': '',
                'type': ''
            }
        )


class ShahkarServiceError(Error):
    def __init__(self, ):
        super().__init__(
            message="Shahkar Service Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'Shahkar Service Error',
                'field': '',
                'type': ''
            }
        )


class UserInfoNotMatched(Error):
    def __init__(self, ):
        super().__init__(
            message="User information is not matched",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'اطلاعات وارد شده تطابق ندارد',
                'field': '',
                'type': ''
            }
        )
