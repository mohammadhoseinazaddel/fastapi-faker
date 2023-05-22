from system.base.exceptions import Error


class CoinAlreadyExists(Error):
    def __init__(self, ):
        super().__init__(
            message="coin with this name already exists",
            errors={}
        )


class CoinNotFound(Error):
    def __init__(self):
        super().__init__(
            message="coin with this name not found",
            errors={
                "code": 422,
                "message": "Invalid Coin Name",
                "field": "coin_name",
                "type": "data-error"
            }
        )


class CoinDoesNotSupported(Error):
    def __init__(self):
        super().__init__(
            message="this coin doesnt supported.",
            errors={
                "code": 422,
                "message": "Invalid Coin Name",
                "field": "coin_name",
                "type": "data-error"
            }
        )


class CoinDoesNotMatchByNetwork(Error):
    def __init__(self):
        super().__init__(
            message="Coin Does Not Match By Network",
            errors={
                "code": 422,
                "message": "کوین یا توکن با شبکه همخوانی ندارد",
                "field": "network_name",
                "type": "data-error"
            }
        )
