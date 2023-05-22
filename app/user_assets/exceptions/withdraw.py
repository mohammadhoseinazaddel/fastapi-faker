from system.base.exceptions import Error


class WithdrawSendRequestFailed(Error):
    def __init__(self, ):
        super().__init__(
            message="Withdraw Send Request Failed",
            errors={
                'code': 422,
                'message': 'متاسفانه ارسال درخواست برداشت با خطا مواجه شد.',
            }
        )
