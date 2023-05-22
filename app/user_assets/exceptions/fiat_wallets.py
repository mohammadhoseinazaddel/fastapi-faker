from starlette import status

from system.base.exceptions  import Error


class UserFiatWalletAlreadyExists(Error):
    def __init__(self, ):
        super().__init__(
            message="user fiat wallet already exists.",
            errors={
                'code': 422,
                'message': '',
            }
        )


class UserFiatWalletDoesNotExists(Error):
    def __init__(self):
        super().__init__(
            message="user fiat wallet does not exists.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': "User fiat wallet doesn't exists",
                'field': '',
                'type': ''
            }
        )


class UserFiatWalletIsMoreThanOne(Error):
    def __init__(self):
        super().__init__(
            message="user fiat wallet is more than one.",
            errors={
                'code': 422,
                'message': '',
            }
        )


class NotEnoughMoney(Error):
    def __init__(self):
        super().__init__(
            message="not enough money.",
            errors={
                'code': 422,
                'message': '',
            }
        )
