from system.base.exceptions  import Error
from fastapi import status


class JibitConnectionError(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit Connection Error",
            errors={
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Jibit Connection Error',
                'field': '',
                'type': 'Jibit.Connection'
            }
        )


class JibitCredentialError(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit Credential Error",
            errors={
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Jibit Credential Error',
                'field': '',
                'type': 'Jibit.Credential'
            }
        )


class JibitServerError(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit Server Error",
            errors={
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Jibit Server Error',
                'field': '',
                'type': 'Jibit.Server'
            }
        )


class JibitUndefinedError(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit Undefined Error",
            errors={
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Jibit Undefined Error',
                'field': '',
                'type': 'Jibit.Undefined'
            }
        )


class JibitUnexpectedErrorInput(Error):
    def __init__(self, ):
        super().__init__(
            message="Jibit Undefined Error",
            errors={
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Jibit Undefined Error',
                'field': '',
                'type': 'Jibit.Undefined'
            }
        )
