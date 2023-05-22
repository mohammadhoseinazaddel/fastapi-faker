from system.base.exceptions  import Error


class UserCryptoWalletAlreadyExists(Error):
    def __init__(self, ):
        super().__init__(
            message="user crypto wallet already exists.",
            errors={
                'code': 422,
                'message': 'کیف پول کریپتویی موجود می باشد',
            }
        )


class UserCryptoWalletDoesNotExists(Error):
    def __init__(self):
        super().__init__(
            message="user crypto wallet does not exists.",
            errors={
                'code': 422,
                'message': 'کیف پول کریپتویی موجود نمی باشد',
            }
        )


class NotEnoughBalance(Error):
    def __init__(self):
        super().__init__(
            message="not enough balance.",
            errors={
                'code': 422,
                'message': 'بالانس کیف پول کریپتویی کافی نمی باشد',
            }
        )


class NotEnoughBlockedAmount(Error):
    def __init__(self):
        super().__init__(
            message="not enough blocked balance.",
            errors={
                'code': 422,
                'message': 'مقدار بالانس بلاک شده کافی نمی باشد',
            }
        )


class NetworkNameDoesNotSupported(Error):
    def __init__(self):
        super().__init__(
            message="this network name doesnt supported.",
            errors={
                "code": 422,
                "message": "Invalid Network",
                "field": "network_name",
                "type": "data-error"
            }
        )


class ExTransactionModelNameIsNotValid(Error):
    def __init__(self):
        super().__init__(
            message="this model name doesnt support for generic foreignkey",
            errors={
                "code": 422,
                "message": "Invalid model name",
                "field": "model_name",
                "type": "data-error"
            }
        )


class BlockTransactionNotMach(Error):
    def __init__(self):
        super().__init__(
            message="This unblock transaction not match with block transaction that sent",
            errors={
                "code": 422,
                "message": "Invalid unblock transaction",
                "field": "block_transaction",
                "type": "not-mach-error"
            }
        )
