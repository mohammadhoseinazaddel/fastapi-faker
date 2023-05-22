import datetime

import pytest

from blockchain.models.transaction import UasBcTransaction
from wallet.exceptions.user_crypto_wallet_exceptions import UserCryptoWalletAlreadyExists, \
    NetworkNameDoesNotSupported, UserCryptoWalletDoesNotExists, NotEnoughBalance, ExTransactionModelNameIsNotValid
from user.models.user_model import UsrUser
from wallet.exceptions.user_crypto_wallet_exceptions import UserCryptoWalletAlreadyExists,\
    NetworkNameDoesNotSupported, UserCryptoWalletDoesNotExists, NotEnoughBalance

from wallet.exceptions.coin_exceptions import CoinDoesNotSupported

from wallet.exceptions.transaction_exceptions import BlockChainTransactionNotFound, \
    BlockChainTransactionIdShouldBeUnique, BlockDecreaseTransactionNotFound, \
    BlockedBalanceShouldBeEqualToDecreaseAmount, DecreaseTransactionAlreadyExists, \
    ExTransactionShouldBeUnique, IncreaseTransactionAlreadyExists

from wallet.interfaces.coin_interface import coin_agent
from wallet.interfaces.user_crypto_wallet_interface import user_crypto_wallet_agent
from wallet.models.crypto_transaction_model import UasCryptoTransaction
from wallet.models.crypto_wallets_model import UasCryptoWallets
from blockchain.models.address import UasAddress


class TestCryptoWalletInterface:

    # class scope fixtures
    @pytest.fixture(scope="function")
    def create_bitcoin_and_ethereum_coins(self, db):
        coin_agent.create_coin('bitcoin', db)
        coin_agent.create_coin('ethereum', db)

    @pytest.fixture(scope='function')
    def create_three_bc_transaction(self, db):
        user = db.query(UsrUser).all()[0]
        bc_address = UasAddress(
            user_id=user.id,
            coin_name='bitcoin',
            network_name='ERC20',
            address='test123',

        )
        db.add(bc_address)
        
        db.flush()

        for i in range(3):
            # create 3 bc transaction obj
            bc_transaction = UasBcTransaction(
                user_id=user.id,
                wallet_address_id=bc_address.id,
                transaction_type='deposit',
                from_address='test_address',
                to_address='test_address',
                amount=1,
                system_status='test',
                balance_verify=True,
                balance_verify_at=datetime.datetime.now(),
            )

            db.add(bc_transaction)
            

    @pytest.fixture(scope='function')
    def create_crypto_wallet(self, db):
        """
            call "initiate_user_and_permissions" first
        """
        user = db.query(UsrUser).all()[0]
        wallet = user_crypto_wallet_agent.create_user_wallet(
            db=db,
            user_id=user.id,
            network_name='ERC20',
            coin_name='bitcoin')
        return wallet

    # tests
    # create_user_wallet
    def test_create_crypto_wallet(
            self,
            db,
            initiate_user_and_permissions,
            create_bitcoin_and_ethereum_coins
    ):
        user = db.query(UsrUser).all()[0]
        user_crypto_wallet_agent.create_user_wallet(
            db=db,
            user_id=user.id,
            network_name='ERC20',
            coin_name='bitcoin')

        wallets = db.query(UasCryptoWallets).filter().all()
        assert len(wallets) == 1

        wallet = wallets[0]
        assert wallet.coin_name == 'bitcoin'
        assert wallet.network_name == 'ERC20'
        assert wallet.user_id == user.id
        assert wallet.balance is None
        assert wallet.froze_amount is None
        assert wallet.blocked_amount is None
        assert wallet.delete_history is None
        assert wallet.created_at is not None
        assert wallet.updated_at is not None
        assert wallet.deleted_at is None

    def test_bad_create_wallet(
            self,
            db,
            initiate_user_and_permissions,
            create_bitcoin_and_ethereum_coins
    ):
        """
            test create crypto wallet exceptions
        """

        user = initiate_user_and_permissions

        with pytest.raises(Exception) as e:
            user_crypto_wallet_agent.create_user_wallet(
                db=db,
                user_id=user.id,
                network_name='ERC20',
                coin_name='bitcoin')
            user_crypto_wallet_agent.create_user_wallet(
                db=db,
                user_id=user.id,
                network_name='ERC20',
                coin_name='bitcoin')
        assert e.type is UserCryptoWalletAlreadyExists

        with pytest.raises(Exception) as e:
            user_crypto_wallet_agent.create_user_wallet(
                db=db,
                user_id=user.id,
                network_name='something',
                coin_name='bitcoin')
        assert e.type is NetworkNameDoesNotSupported

        with pytest.raises(Exception) as e:
            user_crypto_wallet_agent.create_user_wallet(
                db=db,
                user_id=user.id,
                network_name="ERC20",
                coin_name='ada'
            )
        assert e.type is CoinDoesNotSupported

    # delete_wallet_by_id
    def test_delete_wallet_by_id(self,
                                 db,
                                 initiate_user_and_permissions,
                                 create_bitcoin_and_ethereum_coins):
        user = initiate_user_and_permissions
        wallet = user_crypto_wallet_agent.create_user_wallet(user_id=user.id,
                                                                       network_name="ERC20",
                                                                       coin_name="bitcoin",
                                                                       db=db)
        user_crypto_wallet_agent.delete_user_wallet_by_id(wallet_id=wallet.id, db=db)

        deleted_wallet = db.query(UasCryptoWallets).filter(UasCryptoWallets.id == wallet.id).first()

        assert deleted_wallet.deleted_at is not None

    def test_create_same_wallet_after_safe_delete(self,
                                                  db,
                                                  initiate_user_and_permissions,
                                                  create_bitcoin_and_ethereum_coins):
        user = initiate_user_and_permissions
        wallet = user_crypto_wallet_agent.create_user_wallet(
            user_id=user.id,
            network_name="ERC20",
            coin_name="bitcoin",
            db=db
        )
        user_crypto_wallet_agent.delete_user_wallet_by_id(wallet_id=wallet.id, db=db)
        user_crypto_wallet_agent.create_user_wallet(
            user_id=user.id,
            network_name="ERC20",
            coin_name="bitcoin",
            db=db
        )
        wallets = db.query(UasCryptoWallets).filter(UasCryptoWallets.network_name == "ERC20").all()
        assert len(wallets) == 2

    # increase_balance
    def test_increase_balance(self,
                              db,
                              create_bitcoin_and_ethereum_coins,
                              initiate_user_and_permissions,
                              create_crypto_wallet,
                              create_three_bc_transaction,
                              ):
        # test adding 1.176 balance to 0 so the balance should be equal to 1.176
        user = db.query(UsrUser).all()[0]
        bc_transaction = db.query(UasBcTransaction).all()[0]

        wallet = create_crypto_wallet
        user_crypto_wallet_agent.increase_balance(
            user_id=user.id,
            amount=1.176,
            input_unique_id=bc_transaction.id,
            input_type='UasBcTransaction',
            coin_name='bitcoin',
            network_name='ERC20',
            db=db
        )

        assert wallet.balance == 1.176

        all_crypto_transactions = db.query(UasCryptoTransaction).all()
        assert len(all_crypto_transactions) == 1

        crypto_transaction = all_crypto_transactions[0]
        assert crypto_transaction.type == 'increase'
        assert crypto_transaction.input_unique_id == bc_transaction.id
        assert crypto_transaction.input_type == "UasBcTransaction"
        assert crypto_transaction.amount == 1.176
        assert crypto_transaction.crypto_wallet_id == wallet.id
        assert crypto_transaction.created_at is not None
        assert crypto_transaction.updated_at is not None

        assert wallet.balance == 1.176

        # test adding 0.824 balance to 1.176 so the balance should be equal to 2
        new_bc_transaction = db.query(UasBcTransaction).all()[1]
        user_crypto_wallet_agent.increase_balance(
            user_id=user.id,
            amount=0.824,
            input_unique_id=new_bc_transaction.id,
            input_type='UasBcTransaction',
            coin_name='bitcoin',
            network_name='ERC20',
            db=db
        )

        all_crypto_transactions = db.query(UasCryptoTransaction).all()
        assert len(all_crypto_transactions) == 2

        new_crypto_transaction = all_crypto_transactions[1]
        assert new_crypto_transaction.type == 'increase'
        assert new_crypto_transaction.input_unique_id == new_bc_transaction.id
        assert new_crypto_transaction.input_type == "UasBcTransaction"
        assert new_crypto_transaction.amount == 0.824
        assert new_crypto_transaction.crypto_wallet_id == wallet.id
        assert new_crypto_transaction.created_at is not None
        assert new_crypto_transaction.updated_at is not None

        assert wallet.balance == 2

    # TEST BAD INCREASE BALANCE
    def test_bad_increase_balance_with_invalid_ex_model_name(self,
                                                             db,
                                                             create_bitcoin_and_ethereum_coins,
                                                             initiate_user_and_permissions,
                                                             create_crypto_wallet,
                                                             create_three_bc_transaction):
        with pytest.raises(Exception) as e:
            n_user = db.query(UsrUser).all()[0]
            bc_transaction = db.query(UasBcTransaction).all()[0]

            user_crypto_wallet_agent.increase_balance(
                user_id=n_user.id,
                amount=1.176,
                input_unique_id=bc_transaction.id,
                input_type='wrong_name',
                coin_name='bitcoin',
                network_name='ERC20',
                db=db
            )
        assert e.type == ExTransactionModelNameIsNotValid

    def test_bad_increase_balance_with_doesnt_exists_wallet(self,
                                                            db,
                                                            create_bitcoin_and_ethereum_coins,
                                                            initiate_user_and_permissions,
                                                            create_crypto_wallet,
                                                            create_three_bc_transaction):
        with pytest.raises(Exception) as e:
            user = db.query(UsrUser).all()[0]
            bc_transaction = db.query(UasBcTransaction).all()[0]

            wallet = create_crypto_wallet
            user_crypto_wallet_agent.increase_balance(
                user_id=user.id,
                amount=1.176,
                input_unique_id=bc_transaction.id,
                input_type='UasBcTransaction',
                coin_name='ethereum',
                network_name='ERC20',
                db=db
            )
        assert e.type == UserCryptoWalletDoesNotExists

    def test_bad_increase_balance_with_duplicate_transaction(self,
                                                             db,
                                                             create_bitcoin_and_ethereum_coins,
                                                             initiate_user_and_permissions,
                                                             create_crypto_wallet,
                                                             create_three_bc_transaction):
        user = db.query(UsrUser).all()[0]
        bc_transaction = db.query(UasBcTransaction).all()[0]
        with pytest.raises(Exception) as e:
            user_crypto_wallet_agent.increase_balance(
                user_id=user.id,
                amount=1.176,
                input_unique_id=bc_transaction.id,
                input_type='UasBcTransaction',
                coin_name='bitcoin',
                network_name='ERC20',
                db=db
            )
            user_crypto_wallet_agent.increase_balance(
                user_id=user.id,
                amount=1.1,

                # this two fields should be unique together
                input_unique_id=bc_transaction.id,
                input_type='UasBcTransaction',

                coin_name='bitcoin',
                network_name='ERC20',
                db=db
            )
        assert e.type == IncreaseTransactionAlreadyExists

    # block_balance_to_decrease
    def test_block_to_decrease(self,
                               db,
                               initiate_user_and_permissions,
                               create_bitcoin_and_ethereum_coins,
                               create_crypto_wallet,
                               create_three_bc_transaction):
        first_bc_transaction = db.query(UasBcTransaction).all()[0]
        second_bc_transaction = db.query(UasBcTransaction).all()[1]
        user = db.query(UsrUser).all()[0]

        user_crypto_wallet_agent.increase_balance(
            user_id=user.id,
            amount=4,
            input_unique_id=first_bc_transaction.id,
            input_type="UasBcTransaction",
            coin_name='bitcoin',
            network_name='ERC20',
            db=db
        )

        user_crypto_wallet_agent.block_balance_to_decrease(
            user_id=db.query(UsrUser).all()[0].id,
            amount=1.5,
            input_unique_id=second_bc_transaction.id,
            input_type="UasBcTransaction",
            coin_name='bitcoin',
            network_name='ERC20',
            db=db
        )

        transactions = db.query(UasCryptoTransaction).all()
        assert len(transactions) == 2  # increase, block_decrease

        # check the transaction to be created with right values
        block_decrease_transaction = db.query(UasCryptoTransaction).filter(
            UasCryptoTransaction.type == 'block_decrease').first()

        assert block_decrease_transaction.type == 'block_decrease'
        assert block_decrease_transaction.input_unique_id == second_bc_transaction.id
        assert block_decrease_transaction.input_type == "UasBcTransaction"
        assert block_decrease_transaction.amount == 1.5
        assert block_decrease_transaction.crypto_wallet_id is not None

        assert block_decrease_transaction.created_at is not None
        assert block_decrease_transaction.updated_at is not None

        wallet = db.query(UasCryptoWallets).all()[0]

        assert wallet.coin_name == 'bitcoin'
        assert wallet.network_name == "ERC20"
        assert wallet.user_id == user.id
        assert wallet.balance == 2.5
        assert wallet.froze_amount == 0
        assert wallet.blocked_amount == 1.5
        assert wallet.updated_at > wallet.created_at
        assert type(wallet.created_at) is datetime.datetime
        assert type(wallet.updated_at) is datetime.datetime
        assert wallet.delete_history is None
        assert wallet.deleted_at is None

    # TEST BAD BLOCK_TO_DECREASE
    def test_bad_block_to_decrease_without_wallet(self,
                                                  db,
                                                  initiate_user_and_permissions):
        with pytest.raises(Exception) as e:
            user_crypto_wallet_agent.block_balance_to_decrease(
                user_id=1,
                network_name='ERC20',
                coin_name='bitcoin',
                amount=1.2,
                input_unique_id=1,
                input_type="UasBcTransaction",
                db=db
            )
        assert e.type == UserCryptoWalletDoesNotExists

    def test_bad_block_to_decrease_with_invalid_transaction_model_name(self,
                                                                       db,
                                                                       initiate_user_and_permissions,
                                                                       create_bitcoin_and_ethereum_coins,
                                                                       create_crypto_wallet):
        with pytest.raises(Exception) as e:
            user = db.query(UsrUser).all()[0]
            user_crypto_wallet_agent.block_balance_to_decrease(
                user_id=user.id,
                network_name='ERC20',
                coin_name='bitcoin',
                amount=1.2,
                input_unique_id=1,
                input_type="wrong_name",
                db=db
            )
        assert e.type == ExTransactionModelNameIsNotValid

    def test_bad_block_to_decrease_without_bc_transaction(self,
                                                          db,
                                                          initiate_user_and_permissions,
                                                          create_bitcoin_and_ethereum_coins,
                                                          create_crypto_wallet, ):
        with pytest.raises(Exception) as e:
            user_crypto_wallet_agent.block_balance_to_decrease(
                user_id=db.query(UsrUser).all()[0].id,
                network_name='ERC20',
                coin_name='bitcoin',
                amount=1.2,
                input_unique_id=1,
                input_type="UasBcTransaction",
                db=db
            )
        assert e.type == BlockChainTransactionNotFound

    def test_bad_block_to_decrease_without_balance(self,
                                                   db,
                                                   initiate_user_and_permissions,
                                                   create_bitcoin_and_ethereum_coins,
                                                   create_crypto_wallet,
                                                   create_three_bc_transaction):
        with pytest.raises(Exception) as e:
            blockchain_transaction = db.query(UasBcTransaction).all()[0]

            user_crypto_wallet_agent.block_balance_to_decrease(
                user_id=db.query(UsrUser).all()[0].id,
                network_name='ERC20',
                coin_name='bitcoin',
                amount=1.2,
                input_type="UasBcTransaction",
                input_unique_id=blockchain_transaction.id,
                db=db
            )
        assert e.type == NotEnoughBalance

    def test_bad_block_to_decrease_with_not_enough_balance(self,
                                                           db,
                                                           initiate_user_and_permissions,
                                                           create_bitcoin_and_ethereum_coins,
                                                           create_crypto_wallet,
                                                           create_three_bc_transaction):
        """
            Here we have some balance but it's not enough
        """
        with pytest.raises(Exception) as e:
            first_bc_transaction = db.query(UasBcTransaction).all()[0]
            second_bc_transaction = db.query(UasBcTransaction).all()[1]

            user_crypto_wallet_agent.increase_balance(
                user_id=db.query(UsrUser).all()[0].id,
                network_name='ERC20',
                coin_name='bitcoin',
                amount=1.2,
                input_unique_id=first_bc_transaction.id,
                input_type="UasBcTransaction",
                db=db
            )

            user_crypto_wallet_agent.block_balance_to_decrease(
                user_id=db.query(UsrUser).all()[0].id,
                network_name='ERC20',
                coin_name='bitcoin',
                amount=2.2,
                input_unique_id=second_bc_transaction.id,
                input_type="UasBcTransaction",
                db=db
            )
        assert e.type == NotEnoughBalance

    def test_bad_block_to_decrease_with_not_unique_bc_transaction(self,
                                                                  db,
                                                                  initiate_user_and_permissions,
                                                                  create_bitcoin_and_ethereum_coins,
                                                                  create_crypto_wallet,
                                                                  create_three_bc_transaction):
        """
            "bc_transaction_id" that you want to use to create "block_decrease" transaction should not be used before
        """
        first_bc_transaction = db.query(UasBcTransaction).all()[0]

        with pytest.raises(Exception) as e:
            user_crypto_wallet_agent.increase_balance(
                user_id=db.query(UsrUser).all()[0].id,
                network_name='ERC20',
                coin_name='bitcoin',
                amount=1.2,
                input_unique_id=first_bc_transaction.id,
                input_type="UasBcTransaction",
                db=db
            )

            user_crypto_wallet_agent.block_balance_to_decrease(
                user_id=db.query(UsrUser).all()[0].id,
                network_name='ERC20',
                coin_name='bitcoin',
                amount=1.2,
                input_unique_id=first_bc_transaction.id,
                input_type="UasBcTransaction",
                db=db
            )
        assert e.type == ExTransactionShouldBeUnique

    # decrease_balance
    def test_decrease_balance(self,
                              db,
                              initiate_user_and_permissions,
                              create_bitcoin_and_ethereum_coins,
                              create_crypto_wallet,
                              create_three_bc_transaction):
        first_bc_transaction = db.query(UasBcTransaction).all()[0]
        second_bc_transaction = db.query(UasBcTransaction).all()[1]
        user = db.query(UsrUser).all()[0]

        user_crypto_wallet_agent.increase_balance(
            user_id=user.id,
            amount=4,
            input_unique_id=first_bc_transaction.id,
            input_type="UasBcTransaction",
            coin_name='bitcoin',
            network_name='ERC20',
            db=db
        )

        user_crypto_wallet_agent.block_balance_to_decrease(
            user_id=db.query(UsrUser).all()[0].id,
            amount=1.5,
            input_unique_id=second_bc_transaction.id,
            input_type="UasBcTransaction",
            coin_name='bitcoin',
            network_name='ERC20',
            db=db
        )

        user_crypto_wallet_agent.decrease_balance(
            user_id=db.query(UsrUser).all()[0].id,
            amount=1.5,
            input_unique_id=second_bc_transaction.id,
            input_type="UasBcTransaction",
            coin_name='bitcoin',
            network_name='ERC20',
            db=db
        )

        transactions = db.query(UasCryptoTransaction).all()
        assert len(transactions) == 3

        decrease_transaction = db.query(UasCryptoTransaction).filter(UasCryptoTransaction.type == 'decrease').first()
        assert decrease_transaction.type == 'decrease'
        assert decrease_transaction.input_unique_id == second_bc_transaction.id
        assert decrease_transaction.input_type == "UasBcTransaction"
        assert decrease_transaction.amount == 1.5
        assert decrease_transaction.crypto_wallet_id is not None
        assert type(decrease_transaction.created_at) is datetime.datetime
        assert type(decrease_transaction.updated_at) is datetime.datetime
        assert decrease_transaction.updated_at > decrease_transaction.created_at

        wallet = db.query(UasCryptoWallets).all()[0]
        assert wallet.coin_name == 'bitcoin'
        assert wallet.network_name == 'ERC20'
        assert wallet.user_id is not None
        assert wallet.balance == 2.5
        assert wallet.froze_amount == 0
        assert not wallet.blocked_amount
        assert wallet.delete_history is None
        assert type(wallet.created_at) is datetime.datetime
        assert type(wallet.updated_at) is datetime.datetime
        assert wallet.updated_at > wallet.created_at
        assert wallet.deleted_at is None

    def test_bad_decrease_balance_without_wallet(self,
                                                 db,
                                                 initiate_user_and_permissions,
                                                 create_bitcoin_and_ethereum_coins,
                                                 ):
        with pytest.raises(Exception) as e:
            user_crypto_wallet_agent.decrease_balance(
                user_id=db.query(UsrUser).all()[0].id,
                network_name="ERC20",
                coin_name='bitcoin',
                amount=1.22222,
                input_unique_id=1,
                input_type="UasBcTransaction",
                db=db
            )
        assert e.type == UserCryptoWalletDoesNotExists

    def test_bad_decrease_balance_without_blockchain_transaction(self,
                                                                 db,
                                                                 initiate_user_and_permissions,
                                                                 create_bitcoin_and_ethereum_coins,
                                                                 create_crypto_wallet,
                                                                 ):
        with pytest.raises(Exception) as e:
            user_crypto_wallet_agent.decrease_balance(
                user_id=db.query(UsrUser).all()[0].id,
                network_name="ERC20",
                coin_name='bitcoin',
                amount=1.22222,
                input_unique_id=1,
                input_type="UasBcTransaction",
                db=db
            )
        assert e.type == BlockChainTransactionNotFound

    def test_bad_decrease_balance_without_block_transaction(self,
                                                            db,
                                                            initiate_user_and_permissions,
                                                            create_bitcoin_and_ethereum_coins,
                                                            create_crypto_wallet,
                                                            create_three_bc_transaction):
        first_bc_transaction = db.query(UasBcTransaction).all()[0]

        with pytest.raises(Exception) as e:
            user_crypto_wallet_agent.decrease_balance(
                user_id=db.query(UsrUser).all()[0].id,
                network_name="ERC20",
                coin_name='bitcoin',
                amount=1.22222,
                input_unique_id=first_bc_transaction.id,
                input_type="UasBcTransaction",
                db=db
            )
        assert e.type == BlockDecreaseTransactionNotFound

    def test_bad_decrease_balance_with_different_amount_of_block_and_decrease(self,
                                                                              db,
                                                                              initiate_user_and_permissions,
                                                                              create_bitcoin_and_ethereum_coins,
                                                                              create_crypto_wallet,
                                                                              create_three_bc_transaction):
        first_bc_transaction = db.query(UasBcTransaction).all()[0]
        second_bc_transaction = db.query(UasBcTransaction).all()[1]

        user_crypto_wallet_agent.increase_balance(
            user_id=db.query(UsrUser).all()[0].id,
            network_name='ERC20',
            coin_name='bitcoin',
            amount=5,
            input_unique_id=first_bc_transaction.id,
            input_type="UasBcTransaction",
            db=db
        )

        user_crypto_wallet_agent.block_balance_to_decrease(
            user_id=db.query(UsrUser).all()[0].id,
            network_name='ERC20',
            coin_name='bitcoin',
            amount=1.2,
            input_unique_id=second_bc_transaction.id,
            input_type="UasBcTransaction",
            db=db
        )

        with pytest.raises(Exception) as e:
            user_crypto_wallet_agent.decrease_balance(
                user_id=db.query(UsrUser).all()[0].id,
                network_name="ERC20",
                coin_name='bitcoin',
                amount=2.2,
                input_unique_id=second_bc_transaction.id,
                input_type="UasBcTransaction",
                db=db
            )
        assert e.type == BlockedBalanceShouldBeEqualToDecreaseAmount

    def test_bad_decrease_balance_with_create_decrease_transaction_twice(self,
                                                                         db,
                                                                         initiate_user_and_permissions,
                                                                         create_bitcoin_and_ethereum_coins,
                                                                         create_crypto_wallet,
                                                                         create_three_bc_transaction):
        first_bc_transaction = db.query(UasBcTransaction).all()[0]
        second_bc_transaction = db.query(UasBcTransaction).all()[1]

        user_crypto_wallet_agent.increase_balance(
            user_id=db.query(UsrUser).all()[0].id,
            network_name='ERC20',
            coin_name='bitcoin',
            amount=5,
            input_unique_id=first_bc_transaction.id,
            input_type="UasBcTransaction",
            db=db
        )

        user_crypto_wallet_agent.block_balance_to_decrease(
            user_id=db.query(UsrUser).all()[0].id,
            network_name='ERC20',
            coin_name='bitcoin',
            amount=1.2,
            input_unique_id=second_bc_transaction.id,
            input_type="UasBcTransaction",
            db=db
        )

        user_crypto_wallet_agent.decrease_balance(
            user_id=db.query(UsrUser).all()[0].id,
            network_name="ERC20",
            coin_name='bitcoin',
            amount=1.2,
            input_unique_id=second_bc_transaction.id,
            input_type="UasBcTransaction",
            db=db
        )

        with pytest.raises(Exception) as e:
            # decrease again
            user_crypto_wallet_agent.decrease_balance(
                user_id=db.query(UsrUser).all()[0].id,
                network_name="ERC20",
                coin_name='bitcoin',
                amount=1.2,
                input_unique_id=second_bc_transaction.id,
                input_type="UasBcTransaction",
                db=db
            )
        assert e.type == DecreaseTransactionAlreadyExists
