from system.base.exceptions import Error
from fastapi import status


#  User Auth exceptions

class InvalidCredential(Error):
    def __init__(self, ):
        super().__init__(
            message="InvalidCredential",
            errors={
                'code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Invalid Credential.',
                'field': '',
                'type': 'InvalidCredential'
            }
        )


class NotEnoughPermission(Error):
    def __init__(self, ):
        super().__init__(
            message="Not enough permissions",
            errors={
                'code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Not enough permissions.',
                'field': '',
                'type': 'Not enough permissions'
            }
        )

