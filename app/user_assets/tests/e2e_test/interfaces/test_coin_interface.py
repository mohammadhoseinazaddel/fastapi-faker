import pytest
from wallet.exceptions.coin_exceptions import CoinAlreadyExists, CoinNotFound
from wallet.interfaces.coin_interface import coin_agent
from wallet.models.coin_model import Coin


class TestCoinInterface:

    # create_coin method
    def test_bad_create_coin_with_already_exists_exception(self, db):
        with pytest.raises(Exception) as e:
            coin_agent.create_coin(coin_name='bitcoin', session=db)
            coin_agent.create_coin(coin_name='bitcoin', session=db)
        assert e.type is CoinAlreadyExists

    def test_create_coin(self, db):
        created_coin = coin_agent.create_coin(coin_name='bitcoin', session=db)
        found_coin = db.query(Coin).filter(Coin.name == 'bitcoin').first()

        assert found_coin is not None
        assert created_coin == found_coin

    # delete_coin_by_name method
    def test_bad_delete_coin_with_not_found_exception(self, db):
        with pytest.raises(Exception) as e:
            coin_agent.delete_coin_by_name('bitcoin', session=db)

        assert e.type is CoinNotFound

    def test_delete_coin(self, db):
        coin_agent.create_coin(coin_name='bitcoin', session=db)
        coin_agent.delete_coin_by_name(coin_name='bitcoin', session=db)

        found_coin = db.query(Coin).filter(Coin.name == 'bitcoin').first()
        assert found_coin is None

    # find_by_name method
    def test_bad_find_coin_with_not_found_exception(self, db):
        with pytest.raises(Exception) as e:
            coin_agent.find_by_name(coin_name="bitcoin", session=db)

        assert e.type is CoinNotFound

    # def test_find_by_name(self, create_fresh_test_db):
    def test_find_coin_by_name(self, db):
        coin_agent.create_coin(coin_name='bitcoin', session=db)
        found_coin = coin_agent.find_by_name(coin_name='bitcoin', session=db)

        assert found_coin is not None
        assert db.query(Coin).filter(Coin.name == 'bitcoin').first() == found_coin
