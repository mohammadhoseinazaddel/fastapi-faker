from system.base.exceptions import Error
from fastapi import status


class RefundAmountError(Error):
    def __init__(self, ):
        super().__init__(
            message="Refund amount should be less that or equal to order amount",
            errors={
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'مقدار ریفاند باید کوچک تر یا برار مبلغ کل اردر باشد',
                'field': '',
                'type': ''
            }
        )


class OrderStatusNotValidToRefund(Error):
    def __init__(self, ):
        super().__init__(
            message="Order status not valid to refund",
            errors={
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'وضعیت سفارش در حالتی نمی باشد که بتوان ان را ریفاند کرد',
                'field': '',
                'type': ''
            }
        )


class OrderIsRefunding(Error):
    def __init__(self, ):
        super().__init__(
            message="Order is refunding please wait",
            errors={
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'سفارش شما در حال ریفاند شدن می باشد. لطفا منتظر بمانید',
                'field': '',
                'type': ''
            }
        )


class OrderAlreadyRefunded(Error):
    def __init__(self, ):
        super().__init__(
            message="Order already refunded",
            errors={
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'سفارش شما قبلا ریفاند شده است',
                'field': '',
                'type': ''
            }
        )
