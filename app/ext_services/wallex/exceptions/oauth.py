from system.base.exceptions import Error
from fastapi import status


class WallexError(Error):
    def __init__(self, ):
        super().__init__(
            message="Wallex Error",
            errors={
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'در حال حاضر ارتباط با والکس مقدور نمی باشد، لطفا مجددا تلاش نمایید',
                'field': '',
                'type': 'Wallex.Error'
            }
        )


class WallexStateNotFound(Error):
    def __init__(self, ):
        super().__init__(
            message="Wallex Error",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'استیت والکس وجود ندارد',
                'field': '',
                'type': 'Wallex.Error'
            }
        )


class WallexLoginTimeExpired(Error):
    def __init__(self, ):
        super().__init__(
            message="WallexLoginTimeExpired",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'زمان شما برای لاگین با والکس به پایان رسیده است',
                'field': '',
                'type': 'Wallex.Login.Time.Expired'
            }
        )
