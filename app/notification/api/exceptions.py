from system.base.exceptions import Error


class NotificationNotFoundException(Error):
    def __init__(self):
        super().__init__(
            message=f"notification object not found",
            errors={
                'code': 400,
                'message': 'آیتم درخواستی شما وجود ندارد',
            }
        )