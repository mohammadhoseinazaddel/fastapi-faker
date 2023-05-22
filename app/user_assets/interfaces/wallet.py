from sqlalchemy.orm import Session

from ext_services.boton.boton_interface import boton_agent
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.base.mixins import InterfaceLifeCycle
from system.dbs.postgre import SessionLocal
from .crypto_transaction import crypto_transaction_agent
from ..exceptions.bc_address import (InvalidDestinationAddress,
                                     WalletAddressIsNotExist)
from ..models.crypto_withdraw import (CreateCryptoWithdraw,
                                      GetMultiCryptoWithdraw,
                                      UpdateCryptoWithdraw,
                                      crypto_withdraw_crud)
from ..models.wallet_address import (CreateUasAddress, GetMultiUasAddress,
                                     UpdateUasAddress, address_crud)


class AddressInterFace(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = address_crud
        self.boton = boton_agent

    def check_user_has_address(self, db: Session, user_id, coin: str, network: str):
        from user import UserService
        user_sr = UserService()
        user = user_sr.user.find_item_multi(db=db, id=user_id)
        user_wallet_address = self.find_item_multi(
            db=db,
            raise_not_found_exception=False,
            national_code=user.national_code,
            coin_name=coin,
            network_name=network
        )
        if user_wallet_address:
            return user_wallet_address[0]
        else:
            raise WalletAddressIsNotExist

    def check_address_from_blockchain(self, network: str, address: str, memo: str):
        res = self.boton.validate_address(network=network, address=address, memo=memo)
        if not res['status']:
            raise InvalidDestinationAddress


address_agent = AddressInterFace(
    crud=address_crud,
    create_schema=CreateUasAddress,
    update_schema=UpdateUasAddress,
    get_multi_schema=GetMultiUasAddress
)


class WithdrawInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = crypto_withdraw_crud
        self.boton = boton_agent

    def acknowledge_withdraw_request(
            self,
            network: str,
            unique_id: int,
            tx_id: str,
            bundle_id: int,
            boton_ack_status: int,
            db: Session
    ):
        from user_assets import UserAssetsService
        user_asset_sr = UserAssetsService()

        withdraw_record = self.find_item_multi(
            db=db,
            unique_id=unique_id
        )[0]

        #  DOUBLE CHECK: any way, if we pop same item from rabbit queue, nothing need to do
        if boton_ack_status == withdraw_record.ack:
            return 0

        new_status = ''

        if boton_ack_status == 5:
            new_status = 'FAILED'

            # get coin name from wallet address
            wallet_address_rec = user_asset_sr.wallet.address.find_item_multi(
                db=db,
                id=withdraw_record.wallet_address_id
            )[0]

            # unblock user balance
            user_asset_sr.crypto_transaction.unblock_balance(
                user_id=withdraw_record.user_id,
                coin_name=wallet_address_rec.coin_name,
                input_type='withdraw',
                input_unique_id=withdraw_record.id,
                amount=withdraw_record.amount,
                db=db
            )

        elif boton_ack_status == 1:
            new_status = 'PENDING'

        elif boton_ack_status == 0:
            new_status = 'ERROR'
            # an operator should check what happened

        self.update_item(
            db=db,
            find_by={
                'unique_id': unique_id
            },
            update_to={
                'ack': boton_ack_status,
                'tx_id': tx_id,
                'bundle_id': bundle_id,
                'status': new_status
            }
        )
        db.commit()

    def verify_withdraw_request(
            self,
            unique_id: int,
            bundle_id: int,
            fee: float,
            is_identical: int,
            boton_verify_status: int,
            db: Session
    ):
        from user_assets import UserAssetsService
        user_asset_sr = UserAssetsService()

        withdraw_record = self.find_item_multi(
            db=db,
            unique_id=unique_id
        )[0]

        #  DOUBLE CHECK: any way, if we pop same item from rabbit queue, nothing need to do
        if boton_verify_status == withdraw_record.verify:
            return 0

        new_status = ''

        if boton_verify_status == 0:
            new_status = 'ERROR'

        elif boton_verify_status == 1:
            new_status = 'SUCCESS'

            # get coin name from wallet address
            wallet_address_rec = user_asset_sr.wallet.address.find_item_multi(
                db=db,
                id=withdraw_record.wallet_address_id
            )[0]

            # decrease user balance
            user_asset_sr.crypto_transaction.decrease_balance(
                user_id=withdraw_record.user_id,
                coin_name=wallet_address_rec.coin_name,
                input_type='withdraw',
                input_unique_id=withdraw_record.id,
                amount=withdraw_record.amount,
                db=db
            )

        self.update_item(
            db=db,
            find_by={
                'unique_id': unique_id
            },
            update_to={
                'verify': boton_verify_status,
                'is_identical': is_identical,
                'fee': fee,
                'bundle_id': bundle_id,
                'status': new_status
            }
        )
        db.commit()


withdraw_agent = WithdrawInterface(
    crud=crypto_withdraw_crud,
    create_schema=CreateCryptoWithdraw,
    update_schema=UpdateCryptoWithdraw,
    get_multi_schema=GetMultiCryptoWithdraw
)


class WalletInterface(InterfaceLifeCycle):
    def __init__(self):
        self.address = address_agent
        self.crypto_withdraw = withdraw_agent
        self.crypto_transaction = crypto_transaction_agent

    def manage_income_deposit(self, sys_obj_sr: object, boton_sr: object, user_agent: object):
        db = SessionLocal()

        records = boton_sr.deposit.get_not_increase_record(db=db)
        for record in records:
            if record.wallet_address is not None:
                if record.status == 1:
                    # find wallet address
                    wallet = self.address.find_item_multi(
                        db=db,
                        address=record.wallet_address,
                        memo=record.memo,
                        raise_not_found_exception=False
                    )
                    #  if we have not the address, the deposit is not ours
                    if not wallet:
                        raise WalletAddressIsNotExist

                    wallet = wallet[0]

                    # find user based on national code
                    user = user_agent.find_by_national_code(db=db, national_code=wallet.national_code)

                    sys_coin = sys_obj_sr.coin.find_item_multi(
                        db=db,
                        wallex_symbol=record.coin,
                        raise_not_found_exception=False
                    )
                    if sys_coin:
                        sys_coin = sys_coin[0]
                        # increase user balance
                        self.crypto_transaction.increase_balance(
                            user_id=user.id,
                            coin_name=sys_coin.name,
                            input_type='deposit',
                            input_unique_id=record.id,
                            amount=float(record.amount),
                            db=db
                        )
                        record.system_status = boton_sr.deposit.STATUS_INCREASED
            else:
                record.system_status = boton_sr.deposit.STATUS_UNKNOWN

        db.commit()


wallet_agent = WalletInterface()
