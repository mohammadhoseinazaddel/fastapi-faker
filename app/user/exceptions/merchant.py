from system.base.exceptions  import Error
from fastapi import status


#  CRUD exceptions
class MerchantNotFound(Error):
    def __init__(self, ):
        super().__init__(
            message="Merchant not found.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'مرچنت وجود ندارد',
                'field': '',
                'type': ''
            }
        )


class MerchantBankProfileNotFound(Error):
    def __init__(self, ):
        super().__init__(
            message="Merchant bank profile not found.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'برای این مرچنت اطلاعات پروفایل بانک وجود ندارد',
                'field': '',
                'type': ''
            }
        )