from system.base.service import ServiceBase


class UserAssetsService(ServiceBase):
    from sqlalchemy.orm import Session

    def __init__(self):
        from .interfaces.fiat_transactions import fiat_wallet_agent
        from .interfaces.crypto_transaction import crypto_transaction_agent
        from .interfaces.wallex import wallex_agent
        from .interfaces.wallex_transaction import wallex_transaction_agent
        from .interfaces.wallet import wallet_agent

        self.fiat_wallets = fiat_wallet_agent
        self.crypto_transaction = crypto_transaction_agent
        self.wallex = wallex_agent
        self.wallex_transaction = wallex_transaction_agent
        self.wallet = wallet_agent

    def get_total_asset_that_can_be_collateral_in_tmn(self, user_id: int, fund_id: int, db: Session):
        """
            This method also consider asset amount that we also blocked them for this fund as default
            It means it will consider them like they are unblocked
        """
        from system_object import SystemObjectsService

        system_object_sr = SystemObjectsService()

        # In this version we just use crypto assets for collateral
        coins = system_object_sr.coin.find_item_multi(db=db)

        # Total tmn amount that can use as collateral
        asset_value_can_used_as_collateral_tmn = 0

        # Adding asset values of user and also consider ltv
        for coin in coins:
            balance = self.crypto_transaction.get_balance(db=db, user_id=user_id, coin_name=coin.name)
            asset_value_can_used_as_collateral_tmn += balance * coin.ltv * coin.price_in_rial

        # Find all active crypto_blocked_transaction for this fund
        crypto_block_transactions = self.crypto_transaction.find_blocked_transactions_that_didnt_unblocked(
            db=db,
            input_type='OrdFund',
            input_unique_id=fund_id,
            raise_not_found_exception=False
        )

        # Sum of all value of assets that already blocked for this fund
        for block_transaction in crypto_block_transactions:
            asset_value_can_used_as_collateral_tmn += realtime_price_manager.get_asset_price(
                coin_name=block_transaction.crypto_wallet.coin.name,
                asset_balance=block_transaction.amount * block_transaction.crypto_wallet.coin.ltv
            )
        return asset_value_can_used_as_collateral_tmn


user_assets_SR = UserAssetsService()
user_assets_service = UserAssetsService()
