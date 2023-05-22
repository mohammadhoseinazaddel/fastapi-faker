from system.base.exceptions  import Error
from fastapi import status

class TransferFailed(Error):
    def __init__(self, ):
        super().__init__(
            message="Transfer Failed",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'انتقال وجه با خطا مواجه شد',
                'field': 'l',
                'type': 'Transfer.Failed'
            }
        )

