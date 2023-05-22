import uuid

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from user.interfaces.user import UserInterface
from user_assets.api.v1.responses.wallet import user_asset_estimate_RM, deposit_address_RM, withdraw_RM, \
    verify_address_RM

router = APIRouter()


@router.get('/asset-detail',
            response_description="get asset estimate",
            response_model=user_asset_estimate_RM.response_model()
            )
async def get_user_total_asset_estimate(
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["wallet:asset-detail"])
):
    try:
        from user_assets import UserAssetsService
        from system_object import SystemObjectsService

        system_object_sr = SystemObjectsService()
        user_asset_sr = UserAssetsService()

        coins = system_object_sr.coin.find_item_multi(db=db, order_by=('id', 'asc'))
        response_list = []
        for coin in coins:
            balance = user_asset_sr.crypto_transaction.get_balance(db=db, user_id=current_user_id, coin_name=coin.name)
            froze_balance = 0
            blocked_balance = 0
            froze_balance += user_asset_sr.crypto_transaction.get_froze(
                db=db,
                user_id=current_user_id,
                coin_name=coin.name
            )
            blocked_balance += user_asset_sr.crypto_transaction.get_blocked(
                db=db,
                user_id=current_user_id,
                coin_name=coin.name
            )
            decimal_places = None
            if coin.name == 'bitcoin':
                decimal_places = 5
            if coin.name == 'ethereum':
                decimal_places = 3
            if coin.name == 'tether':
                decimal_places = 2
            response_list.append(
                {
                    'name': coin.name,
                    'total_balance': round(froze_balance + balance + blocked_balance, decimal_places),
                    'balance': round(balance, decimal_places),
                    'balance_in_tmn': coin.price_in_rial * (froze_balance + balance + blocked_balance) / 10,
                    'balance_in_usdt': round(coin.price_in_usdt * (froze_balance + balance + blocked_balance), 2),
                    'symbol': coin.symbol,
                    'logo_address': coin.logo_address,
                    'name_fa': coin.fa_name,
                    'froze_balance': round(froze_balance, decimal_places),
                    'coin_price_usdt': coin.price_in_usdt,
                    'coin_price_tmn': coin.price_in_rial / 10
                }
            )
        user_asset_estimate_RM.status_code(200)
        return user_asset_estimate_RM.response(response_list)
    except Exception as e:
        db.rollback()
        return user_asset_estimate_RM.exception(e)


@router.get("/deposit",
            response_model=deposit_address_RM.response_model(),
            response_description="Get Your Deposit Address By Coin Name and Network Name"
            )
def get_deposit_address(
        coin_name: str,
        network_name: str,
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["wallet:address:deposit"])
):
    try:
        from system_object import SystemObjectsService
        from user_assets import UserAssetsService
        from ext_services.boton.boton_interface import boton_agent
        from user.interfaces.user_interface import user_agent

        sys_obj_sr = SystemObjectsService()
        user_asset_sr = UserAssetsService()

        # check if coin validity
        sys_obj_sr.coin.validate_coin_and_network(
            db=db,
            coin=coin_name,
            network=network_name
        )

        national_code = user_agent.check_user_national_code_validity(
            db=db,
            user_id=current_user_id
        )['national_code']

        # check if we have got the address before
        address_rec = user_asset_sr.wallet.address.find_item_multi(
            db=db,
            raise_not_found_exception=False,
            national_code=national_code,
            coin_name=coin_name,
            network_name=network_name
        )

        if address_rec:
            address_rec = address_rec[0]

            deposit_address_RM.status_code(200)
            return deposit_address_RM.response(address_rec)

        else:
            res = boton_agent.get_address_from_blockchain(
                network=network_name,
                user_id=int(str(uuid.uuid4().int >> 110))
                # IMPORTANT: we send national_code as user_id in order to get blockchain address
            )

            address_rec = user_asset_sr.wallet.address.add_item(
                db=db,
                user_id=current_user_id,
                national_code=national_code,
                coin_name=coin_name,
                network_name=network_name,
                address=res['result']['address']
            )
            deposit_address_RM.status_code(200)
            return deposit_address_RM.response(res['result'])

    except Exception as e:
        return deposit_address_RM.exception(e)


@router.get('/verify-address',
            response_model=verify_address_RM.response_model(),
            response_description='You Can Find Given Address is Verified or Not'
            )
def verify_address(
        network: str,
        address: str,
        memo: str = None,
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["wallet:address:verify"])
):
    try:
        from ext_services.boton.boton_interface import boton_agent
        res = boton_agent.validate_address(network=network, address=address, memo=memo)

        verify_address_RM.status_code(200)
        return verify_address_RM.response({
            'address': address,
            'is_valid': res['status']
        })

    except Exception as e:
        return verify_address_RM.exception(e)


@router.post("/withdraw",
             response_model=withdraw_RM.response_model(),
             response_description="Withdraw Request"
             )
def withdraw_request(
        request_model: withdraw_RM.request_model() = Depends(withdraw_RM.request_model()),
        db: Session = Depends(get_db),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["wallet:withdraw"])
):
    try:
        coin = request_model.coin
        address = request_model.address
        network = request_model.network
        amount = request_model.amount
        memo = request_model.memo

        from user_assets import UserAssetsService
        from system_object import SystemObjectsService
        from ext_services.boton.boton_interface import boton_agent
        from user.interfaces.user_interface import user_agent

        from user_assets.exceptions.bc_address import InvalidDestinationAddress

        user_asset_sr = UserAssetsService()
        sys_obj_sr = SystemObjectsService()

        # check if coin validity
        sys_obj_sr.coin.validate_coin_and_network(
            db=db,
            coin=coin,
            network=network
        )

        # check if user has enough balance
        user_asset_sr.crypto_transaction.check_user_enough_balance(
            db=db,
            user_id=current_user_id,
            coin=coin,
            amount=amount
        )

        # get user wallet address
        user_wallet_address = user_asset_sr.wallet.address.check_user_has_address(
            db=db,
            user_id=current_user_id,
            coin=coin,
            network=network,
        )

        # destination address validation
        user_asset_sr.wallet.address.check_address_from_blockchain(
            network=network,
            address=address,
            memo=memo
        )

        # withdraw request record
        withdraw_rq_record = user_asset_sr.wallet.crypto_withdraw.add_item(
            db=db,
            user_id=current_user_id,
            wallet_address_id=user_wallet_address.id,
            from_address=user_wallet_address.address,
            from_memo=user_wallet_address.memo,
            to_address=address,
            to_memo=memo,
            amount=amount,
        )
        db.commit()
        withdraw_rq_record.unique_id = int(str(withdraw_rq_record.id) + str(uuid.uuid4().int >> 110))
        db.commit()

        # block user balance
        user_asset_sr.crypto_transaction.block_balance(
            user_id=current_user_id,
            coin_name=coin,
            input_type='withdraw',
            input_unique_id=withdraw_rq_record.id,
            amount=amount,
            db=db
        )

        # send withdraw request to rabbit
        try:
            rabbit_res = boton_agent.submit_withdraw(
                unique_id=withdraw_rq_record.unique_id,
                network=network,
                address=address,
                amount=amount,
                coin=sys_obj_sr.coin.find_item_multi(db=db, name=coin)[0].wallex_symbol,
                memo=memo
            )
            if rabbit_res:
                user_asset_sr.wallet.crypto_withdraw.update_item(
                    db=db,
                    find_by={"id": withdraw_rq_record.id},
                    update_to={"status": "REGISTERED"}
                )
        except Exception as e:
            # unblock user balance
            user_asset_sr.crypto_transaction.unblock_balance(
                user_id=current_user_id,
                coin_name=coin,
                input_type='withdraw',
                input_unique_id=withdraw_rq_record.id,
                amount=amount,
                db=db
            )
            user_asset_sr.wallet.crypto_withdraw.update_item(
                db=db,
                find_by={"id": withdraw_rq_record.id},
                update_to={"status": "REGISTER_ERROR"}
            )
            db.commit()
            # raise WithdrawSendRequestFailed

        withdraw_RM.status_code(200)
        return withdraw_RM.response({'trace_id': withdraw_rq_record.trace_id})

    except Exception as e:
        # db.rollback()
        return withdraw_RM.exception(e)
