from typing import List

from sqlalchemy.orm import Session

from ext_services.wallex.interfaces.price import WallexPriceInterface
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.dbs.postgre import SessionLocal
from ..exceptions.coin import CoinNotFound, CoinDoesNotMatchByNetwork
from ..models.coin import coins_crud, SoCoin, CreateCoin, UpdateCoin, GetCoinMulti


class CoinInterface(InterfaceBase):

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        from ..exceptions import coin as coin_exceptions
        from ..models.schemas import coin as coin_schemas
        self.crud = coins_crud
        self.model = SoCoin
        self.exceptions = coin_exceptions
        self.schemas = coin_schemas
        self.wallex_price = WallexPriceInterface()

    def update_coin_price(self) -> List:
        print('start update coins price')
        db = SessionLocal()
        price_json = self.wallex_price.get_otc_price_list()['result']
        coins = self.find_item_multi(db=db)
        price_list = []
        for item in coins:
            item_price_in_tmn = float(price_json[item.wallex_symbol + 'TMN']['stats']['lastPrice'])
            if not item.wallex_symbol == 'USDT':
                item_price_in_usdt = float(price_json[item.wallex_symbol + 'USDT']['stats']['lastPrice'])
            else:
                item_price_in_usdt = 1

            self.update_item(
                db=db,
                find_by={'id': item.id},
                update_to={'price_in_rial': item_price_in_tmn * 10, 'price_in_usdt': item_price_in_usdt}
            )

        db.commit()
        db.close()

        return price_list

    def validate_coin_and_network(self, db: Session, coin: str, network: str):
        coin = self.find_item_multi(db=db, name=coin)[0]
        if coin:
            if network not in list(coin.networks.values()):
                raise CoinDoesNotMatchByNetwork
        else:
            raise CoinNotFound


coin_agent = CoinInterface(
    crud=coins_crud,
    create_schema=CreateCoin,
    update_schema=UpdateCoin,
    get_multi_schema=GetCoinMulti
)
