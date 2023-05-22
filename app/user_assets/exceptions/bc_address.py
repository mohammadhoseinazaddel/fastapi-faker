from system.base.exceptions import Error


class UserCryptoWalletAddressExist(Error):
    def __init__(self, ):
        super().__init__(
            message="user crypto wallet address already exists.",
            errors={
                'code': 422,
                'message': 'ادرس کریپتو ولت در حال حاضر وجود دارد',
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


class WalletAddressIsNotExist(Error):
    def __init__(self):
        super().__init__(
            message="this wallet address is not found",
            errors={
                "code": 422,
                "message": "ادرس ولت وجود ندارد",
                "field": "wallet_address",
                "type": "data-error"
            }
        )


class InvalidDestinationAddress(Error):
    def __init__(self, ):
        super().__init__(
            message="Invalid Destination Address",
            errors={
                'code': 422,
                'message': 'آدرس مقصد نامعتبر است.',
            }
        )
