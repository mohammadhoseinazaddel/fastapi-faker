from starlette import status

from system.base.exceptions  import Error


class PostPayNeedDebtId(Error):
    def __init__(self, ):
        super().__init__(
            message=f"Order with this merchant id and merchant_order_id already exists",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': f'Order of this merchant with this merchant_order_id already exists',
                'field': 'merchant_order_id',
                'type': 'unique_error'
            }
        )


class FundNotFound(Error):
    def __init__(self, ):
        super().__init__(
            message="Fund with this fund id not found",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': f'Fund with this fund_id not found',
                'field': '',
                'type': 'not-found'
            }
        )


class NothingToRepay(Error):
    def __init__(self, ):
        super().__init__(
            message="No debt or loan to repay",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'هیچ بدهی قابل پرداختی وجود ندارد',
                'field': '',
                'type': 'not-found'
            }
        )


class OrderHaveExtraMoneyToPay(Error):
    def __init__(self):
        super().__init__(
            message="Order have Extra money to pay so this api is not usable for this kind of orders",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'این سفارش نیاز به پرداخت ریالی از درگاه بانکی دارد',
                'field': '',
                'type': 'not-found'
            }
        )


class CollateralIsNotEnough(Error):
    def __init__(self):
        super().__init__(
            message="Collateral for this order is not enough",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'مقدار وثیقه شما برای این سفارش کافی نمی باشد و باید ان را افزایش دهید',
                'field': '',
                'type': 'not-found'
            }
        )


class CreditIsNotEnough(Error):
    def __init__(self):
        super().__init__(
            message="Credit is not enough",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'کردیت شما کافی نمی باشد',
                'field': '',
                'type': 'not-found'
            }
        )