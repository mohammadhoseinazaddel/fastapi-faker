from starlette import status

from system.base.exceptions import Error


class BlockChainTransactionNotFound(Error):
    def __init__(self):
        super().__init__(
            message="Blockchain transaction with this id not found",
            errors={
                'code': 422,
                'message': 'تراکنش بلاکچینی موجود نمی باشد',
            }
        )


class BlockChainTransactionIdShouldBeUnique(Error):
    def __init__(self):
        super().__init__(
            message="A transaction with this bc_transaction id already exists",
            errors={
                'code': 422,
                'message': '',
            }
        )


class ExTransactionShouldBeUnique(Error):
    def __init__(self):
        super().__init__(
            message="A transaction with this ex_transaction id and input_type already exists",
            errors={
                'code': 422,
                'message': '',
            }
        )


class BlockDecreaseTransactionNotFound(Error):
    def __init__(self):
        super().__init__(
            message="You should block balance before decrease the balance",
            errors={
                'code': 422,
                'message': '',
            }
        )


class BlockFreezeTransactionNotFound(Error):
    def __init__(self):
        super().__init__(
            message="You should block balance before freeze the balance",
            errors={
                'code': 422,
                'message': '',
            }
        )


class BlockedBalanceShouldBeEqualToDecreaseAmount(Error):
    def __init__(self):
        super().__init__(
            message="Amount of blocked transaction should be equal to amount of decrease transaction",
            errors={
                'code': 422,
                'message': '',
            }
        )


class BlockedBalanceShouldBeEqualToFreezeAmount(Error):
    def __init__(self):
        super().__init__(
            message="Amount of blocked transaction should be equal to amount of freeze transaction",
            errors={
                'code': 422,
                'message': '',
            }
        )


class DecreaseTransactionAlreadyExists(Error):
    def __init__(self):
        super().__init__(
            message="Decrease transaction already exists for this bc_transaction id",
            errors={
                'code': 422,
                'message': '',
            }
        )


class IncreaseTransactionAlreadyExists(Error):
    def __init__(self):
        super().__init__(
            message="Increase transaction already exists for this bc_transaction id",
            errors={
                'code': 422,
                'message': '',
            }
        )


class FreezeTransactionAlreadyExists(Error):
    def __init__(self):
        super().__init__(
            message="Freeze transaction already exists for this ex_transaction",
            errors={
                'code': 422,
                'message': '',
            }
        )


class TransactionAlreadyUsed(Error):

    def __init__(self):
        super().__init__(
            message="Crypto transaction with this 'type', 'input_type', 'input_unique_id' already exists",
            errors={
                'code': 422,
                'message': '',
            }
        )


class NotEnoughAsset(Error):
    def __init__(self):
        super().__init__(
            message="Asset is not enough",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'مقدار دارایی شما کافی نمیباشد',
                'field': '',
                'type': 'not-found'
            }
        )


class TransactionNotFound(Error):
    def __init__(self):
        super().__init__(
            message="Crypto Wallet Transaction Not Found",
            errors={
                'code': 422,
                'message': '',
            }
        )


class UnblockTransactionNeedsBlockTransactionId(Error):
    def __init__(self):
        super().__init__(
            message="Unblock transaction needs block transaction id",
            errors={
                'code': 422,
                'message': '',
            }
        )


class ThisBlockedTransactionAlreadyUnblocked(Error):
    def __init__(self):
        super().__init__(
            message="This block transaction already unblocked",
            errors={
                'code': 422,
                'message': '',
            }
        )


class UserBalanceIsNotEnough(Error):
    def __init__(self, ):
        super().__init__(
            message="User Balance Is Not Enough",
            errors={
                'code': 422,
                'message': 'موجودی کاربر برای انتقال کوین کافی نیست',
            }
        )
