import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from user.interfaces.user import UserInterface
from finance.finance_service import FinanceService
from .... import UserService
from ....exceptions.merchant import MerchantBankProfileNotFound
from system.dbs.postgre import SessionLocal


@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()


def test_get_merchant_info_with_login(monkeypatch, db: Session):
    # Create a merchant user with no bank profile
    user_sr = UserService()
    merchant = user_sr.merchant.add_item(
        db=db,
        name='test',
        name_fa='تست',
        url='https://www.alibaba.ir/',
        logo_background_color='#FFEBE4',

    )
    user = user_sr.user.add_item(
        db=db,
        username="test_user",
        password="password",
        email="test@example.com",
        merchant_name="test",
        merchant_id=merchant.id
    )
    user_sr.user.add_to_merchant(user_id=user.id, merchant_id=merchant.id, db=db)
    fn_sr = FinanceService()
    bank_profile = fn_sr.bank_profile.add_item(
        db=db,
        merchant_id=user.merchant.id,
        is_default=True,
        account_no="12345678",
        iban="GB29 NWBK 6016 1331 9268 19",
        bank_name="Test Bank",
        user_id=user.id,
    )
    mock_find_by_id = Mock(return_value=user)
    monkeypatch.setattr(UserInterface, "find_by_id", mock_find_by_id)

    # Call the function under test
    data = UserInterface.get_merchant_info_with_login(current_user_id=user.id, db=db)

    # Check the result
    assert data["name"] == user.merchant.name
    assert data["name_fa"] == user.merchant.name_fa
    assert data["logo_address"] == user.merchant.logo_address
    assert data["logo_background_color"] == user.merchant.logo_background_color
    assert data["bank_account_number"] == bank_profile.account_no
    assert data["bank_iban"] == bank_profile.iban
    assert data["bank_name"] == bank_profile.bank_name


def test_get_merchant_info_with_login_no_bank_profile(db: Session):
    # Create a merchant user with no bank profile
    user_sr = UserService()
    merchant = user_sr.merchant.add_item(
        db=db,
        name='test',
        name_fa='تست',
        url='https://www.alibaba.ir/',
        logo_background_color='#FFEBE4',

    )
    user = user_sr.user.add_item(
        db=db,
        username="test_user",
        password="password",
        email="test@example.com",
        merchant_name="test",
        merchant_id=merchant.id
    )
    user_sr.user.add_to_merchant(user_id=user.id, merchant_id=merchant.id, db=db)
    rudimentary_group = user_sr.group.find_item_multi(
        db=db,
        name='rudimentary'
    )[0]

    user_sr.user.add_to_group(
        user_id=user.id,
        group_id=rudimentary_group.id,
        db=db
    )

    # Call the function under test
    with pytest.raises(MerchantBankProfileNotFound):
        UserInterface.get_merchant_info_with_login(current_user_id=user.id, db=db)
