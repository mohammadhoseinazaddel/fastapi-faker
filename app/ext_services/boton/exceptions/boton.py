from starlette import status

from system.base.exceptions import Error


class WallexBotonAddressManagementError(Error):
    def __init__(self, jibit_message=None):
        super().__init__(
            message="Wallex Boton Address ManagementError",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای والکس: سرویس مدیریت آدرس بلاک چین',
                'field': '',
                'type': 'Wallex.Boton.Address.Management'
            }
        )


class WallexBotonAddressVerifiactionError(Error):
    def __init__(self, jibit_message=None):
        super().__init__(
            message="Wallex Boton Address Verifiaction Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'خطای والکس: سرویس تایید آدرس بلاک چین',
                'field': '',
                'type': 'Wallex.Boton.Address.Verifiaction'
            }
        )