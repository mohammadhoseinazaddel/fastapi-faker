from fastapi import status

from system.base.exceptions import Error


#  CRUD exceptions
class OrderNotFound(Error):
    def __init__(self, ):
        super().__init__(
            message="Order not found.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'سفارش پرداخت وجود ندارد',
                'field': '',
                'type': ''
            }
        )


class OrderAlreadyExists(Error):
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


class OrderTypeIsNotValid(Error):
    def __init__(self, ):
        from finance.models.fnc_order import order_crud
        super().__init__(
            message=f"Order type is not valid. Valid types are {[type_name for type_name in order_crud.ORDER_VALID_TYPES]}",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': f'Order type is not valid. Valid types are {[type_name for type_name in order_crud.ORDER_VALID_TYPES]}',
                'field': 'type',
                'type': 'type_name_invalid'
            }
        )


class OrderAlreadyHaveUserId(Error):
    def __init__(self, ):
        super().__init__(
            message="This order obj already have user",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': "This order already have user_id",
                'field': 'user_id',
                'type': 'user_id_exists'
            }
        )


class OrderAlreadyProcessed(Error):
    def __init__(self):
        super().__init__(
            message="This order has been processed before",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': "این اردر خرید قبلا پردازش شده است",
                'field': 'order',
                'type': 'order_already_processed'
            }
        )


class UnAuthorized(Error):
    def __init__(self):
        super().__init__(
            message="",
            errors={
                'code': status.HTTP_403_FORBIDDEN,
                'message': 'UnAuthorized Error',
                'field': '',
                'type': 'un-authorized'
            }
        )


class InvalidOrderStatus(Error):
    def __init__(self):
        super().__init__(
            message="The current status is invalid for this action",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'Invalid Order Status',
                'field': '',
                'type': 'Invalid.Order.Status'
            }
        )


class OrderHasBeenExpired(Error):
    def __init__(self, ):
        super().__init__(
            message="Order has been expired",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'زمان زیادی از ثبت سفارش گذشته است و سفارش منقضی شده است',
            }
        )


class OrderIsNotAuthenticate(Error):
    def __init__(self, ):
        super().__init__(
            message="Order has been expired",
            errors={
                'code': status.HTTP_403_FORBIDDEN,
                'message': 'دسترسی به این سفارش امکان پذیر نیست',
            }
        )


class OrderIsProcessing(Error):
    def __init__(self, ):
        super().__init__(
            message="Order has been expired",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'سفارش در حال پردازش است',
            }
        )


class OrderActionNotSupported(Error):
    def __init__(self, ):
        super().__init__(
            message="Order has been expired",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'عملیات مورد نظر مجاز نمی باشد',
            }
        )


class OrderActionTimeExpired(Error):
    def __init__(self, ):
        super().__init__(
            message="Order has been expired",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'زمان زیادی از ثبت سفارش گذشته است و امکان تغییر عملیات وجود ندارد',
            }
        )


class OrderActionIsNotUnverified(Error):
    def __init__(self, ):
        super().__init__(
            message="Order has been expired",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'عملیات دیگری بر روی سفارش انجام شده است',
            }
        )


class OrderStatusNotSuccess(Error):
    def __init__(self, ):
        super().__init__(
            message="Order has been expired",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'پردازش سفارش تکمیل نشده است',
            }
        )
