from starlette import status

from system.base.exceptions import Error


class CommissionNotFound(Error):
    def __init__(self, ):
        super().__init__(
            message="Order has been expired",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'نوع کمیسیون درخواستی وجود ندارد',
            }
        )
