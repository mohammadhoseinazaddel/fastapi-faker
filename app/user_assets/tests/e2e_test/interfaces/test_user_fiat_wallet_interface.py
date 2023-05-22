import pytest
from user.exceptions.user_exceptions import UserNotFound
from user.models.group_and_scopes import UsrGroup
from user.models.user_model import UsrUser
from user.schemas.user import AdminUserCreate
from wallet.exceptions.user_fiat_wallet_exceptions import UserFiatWalletAlreadyExists
from wallet.interfaces.user_fiat_wallet_interface import user_fiat_wallet_agent
from wallet.models import UserFiatWallets


class TestUserFiatWalletInterface:
    pass

    def test_bad_create_user_fiat_wallet_with_user_not_found_exception(self,
                                                                       db,
                                                                       initiate_user_and_permissions
                                                                       ):
        # create another user because user_fiat_wallet will create after initiate user and, we will get
        # user_fiat_wallet_already_exists error

        group = db.query(UsrGroup).all()[0]
        first_admin_user = AdminUserCreate(
            first_name="Wallex",
            last_name="Finance",
            email='test@test.com',
            mobile='09123456781',
            username='test',
            password='test@test',
            national_code='0021111111',
            birth_date="1366/01/01"
        )
        user_to_insert = UsrUser(db=db, user=first_admin_user, group_id=group.id)
        db.add(user_to_insert)
        
        db.flush()

        with pytest.raises(Exception) as e:
            user_fiat_wallet_agent.create_user_fiat_wallet(user_id=user_to_insert.id + 1, session=db)
        assert e.type == UserNotFound

    def test_bad_create_user_fiat_wallet_with_user_fiat_wallet_already_exists_exception(self,
                                                                                        db,
                                                                                        initiate_user_and_permissions):
        user = db.query(UsrUser).all()[0]
        with pytest.raises(Exception) as e:
            user_fiat_wallet_agent.create_user_fiat_wallet(user_id=user.id, session=db)
            user_fiat_wallet_agent.create_user_fiat_wallet(user_id=user.id, session=db)
        assert e.type == UserFiatWalletAlreadyExists

    def test_create_user_fiat_wallet(self, db, initiate_user_and_permissions):
        # user_fiat_wallet will create for the user after initiate user

        wallets = db.query(UserFiatWallets).all()
        user = db.query(UsrUser).filter(UsrUser.id == wallets[0].user_id).first()

        assert len(wallets) == 1

        wallet = wallets[0]

        assert wallet.user_id == user.id
        assert wallet.amount is None
        assert wallet.froze_amount is None
        assert wallet.blocked_amount is None

        assert wallet.created_at is not None
        assert wallet.updated_at is not None

        assert wallet.delete_history is None
        assert wallet.disabled_at is None
