import json
from datetime import datetime

from sqlalchemy.orm import Session

from ext_services.wallex.interfaces.login import wallex_login_agent
from ext_services.wallex.interfaces.pay import wallex_pay_agent
from system.base.interface import InterfaceLifeCycle
from system.config import settings
from system.dbs.redis import redis_client, BaseRedis
from .wallex_transaction import wallex_transaction_agent


class WallexInterface(InterfaceLifeCycle):

    def __init__(self):
        self.transactions = wallex_transaction_agent
        self.redis = redis_client
        self.test_redis = BaseRedis(db=5)

    @staticmethod
    def check_user_wallex_connected(db: Session, user_id: int):
        wallex_user_record = wallex_login_agent.find_item_multi(
            db=db,
            user_id=user_id,
            raise_not_found_exception=False,
            order_by=('created_at', 'desc')
        )
        if wallex_user_record:
            return wallex_user_record[0]
        else:
            return False

    def get_user_asset(self, db: Session, user_id: int, use_cache: bool = True):
        wallex_user_record = self.check_user_wallex_connected(db=db, user_id=user_id)
        if wallex_user_record:
            if use_cache:
                obj_as_byte = self.redis.get(f'{"wallex_users_assets" + ":" + wallex_user_record.wallex_user_id}')
                if obj_as_byte:
                    wallex_users_assets_decode = obj_as_byte.decode("utf-8")
                    wallex_users_assets = json.loads(wallex_users_assets_decode)
                    if (datetime.now().timestamp() - wallex_users_assets['updated_time']) / 60 <= 15:
                        return {
                            'wallex_user_id': wallex_users_assets['wallex_user_id'],
                            'wallpay_user_id': wallex_users_assets['wallpay_user_id'],
                            'asset_balance': wallex_users_assets['asset_balance'],
                            'updated_time': wallex_users_assets['updated_time']
                        }
                    else:
                        balances = self._get_online_user_asset(db=db, access_token=wallex_user_record.access_token)
                        return self._update_asset_info_redis(
                            wallex_user_id=wallex_user_record.wallex_user_id,
                            user_id=wallex_user_record.user_id,
                            balances=balances
                        )
                else:
                    balances = self._get_online_user_asset(db=db, access_token=wallex_user_record.access_token)
                    return self._update_asset_info_redis(
                        wallex_user_id=wallex_user_record.wallex_user_id,
                        user_id=wallex_user_record.user_id,
                        balances=balances
                    )
            else:
                balances = self._get_online_user_asset(db=db, access_token=wallex_user_record.access_token)
                return self._update_asset_info_redis(
                    wallex_user_id=wallex_user_record.wallex_user_id,
                    user_id=wallex_user_record.user_id,
                    balances=balances
                )
        else:
            return {
                'wallex_user_id': None,
                'wallpay_user_id': user_id,
                'asset_balance': None,
                'updated_time': datetime.now()
            }

    @staticmethod
    def _get_online_user_asset(db: Session, access_token: str):
        wallex_user_info = wallex_login_agent.get_wallex_user_info(
            db=db,
            access_token=access_token
        ).dict()
        user_balance = []
        balances_details = wallex_user_info['balances_details']
        for balance in balances_details:
            if balance['total'] > 0:
                user_balance.append({
                    'symbol': balance['symbol'],
                    'total': balance['total'],
                    'freeze': balance['freeze'],
                    'available': balance['available']
                })
        return user_balance

    def _update_asset_info_redis(self, wallex_user_id: str, user_id: str, balances: list):
        user_asset_key = "wallex_users_assets" + ":" + wallex_user_id
        asset_info = {
            'wallex_user_id': wallex_user_id,
            'wallpay_user_id': user_id,
            'asset_balance': balances,
            'updated_time': datetime.now().timestamp()
        }
        self.redis.set(user_asset_key, json.dumps(asset_info))
        return asset_info

    def order_request_block_asset(
            self,
            db: Session,
            block_asset: list,
            user_id: int,
            order_uuid: str,
            input_type: str,
            input_unique_id: int,
            callback_type: str,  # only support the pay-order type at this time
    ):

        # check callback type
        supported_callbacks = ['pay-order']
        if callback_type not in supported_callbacks:
            raise SystemError(f'callback type {callback_type} is not supported')

        # find wallex user
        wallex_user_record = wallex_login_agent.find_item_multi(db=db, user_id=user_id)[0]

        # check wallex user asset balance for block requset
        if wallex_user_record:
            balances = self._get_online_user_asset(db=db, access_token=wallex_user_record.access_token)
            assets = []
            for block in block_asset:
                for balance in balances:
                    if block['wallex_symbol'] == balance['symbol']:
                        if block['used_balance'] <= balance['available']:
                            if block['used_balance'] > 0:
                                assets.append({
                                    'currency': block['wallex_symbol'],
                                    'amount': block['used_balance']
                                })
                        else:
                            print('dont have enough available amount')
                            raise SystemError('dont have enough available amount', {
                                'currency': block['currency'],
                                'requested_amount': block['amount'],
                            })

            # create wallex pay request record
            pay_record = wallex_pay_agent.add_item(
                db=db,
                input_type=input_type,
                input_unique_id=input_unique_id,
                assets=assets,
                wallex_user_id=wallex_user_record.wallex_user_id,
                user_id=user_id,
            )

            # create callback url and update in pay request record
            callback_url = settings.WALLPAY_BASE_URL + '/api/v1/user-assets/wallex/callback/' + str(pay_record.uuid)
            wallex_pay_agent.update_item(
                db=db,
                find_by={'id': pay_record.id},
                update_to={'callback_url': callback_url}
            )

            # call wallex create request api for get transaction id
            res = wallex_pay_agent.api_create_request(
                assets=assets,
                user_id=pay_record.wallex_user_id,
                order_id=order_uuid,
                state=callback_type,
                callback_url=callback_url
            )

            trans_id = res['result']['token']
            redirect_url = res['result']['redirect_url']

            # update token field in pay record
            wallex_pay_agent.update_item(
                db=db,
                find_by={'id': pay_record.id},
                update_to={
                    'token': trans_id,
                    'redirect_url': redirect_url,
                    'state': callback_type,
                }
            )

            # return transaction id that get from wallex
            return trans_id
        else:
            print('wallex user id not found')
            raise SystemError('wallex user id not found')

    def cancel_wallex_pay_request(
            self,
            db: Session,
            token: str,
            user_id: int,
            input_type: str,
            input_unique_id: int,
    ):
        wallex_pay_record = wallex_pay_agent.find_item_multi(db=db, token=token)[0]
        wallex_pay_status = wallex_pay_record.status

        if wallex_pay_status == wallex_pay_agent.STATUS_UNVERIFIED:
            wallex_pay_agent.api_reject_request(token=token)
            result = self.transactions.find_blocked_coins(
                db=db,
                input_type=input_type,
                input_unique_id=input_unique_id
            )
            for coin_name, balance in result.items():
                if balance:
                    self.transactions.unblock_balance(
                        user_id=user_id,
                        coin_name=coin_name,
                        input_type=input_type,
                        input_unique_id=input_unique_id,
                        amount=balance,
                        db=db
                    )


wallex_agent = WallexInterface()
