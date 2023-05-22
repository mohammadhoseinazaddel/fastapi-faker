from fastapi import (
    Depends,
    APIRouter)
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from utils import ResponseManager
from ..schemas.coin import *

router = APIRouter()

coin_info_RM = ResponseManager(
    request_model=None,
    response_model=CoinInfoResponse,
    pagination=False,
    is_mock=False
)


@router.get(
    "/info",
    response_model=coin_info_RM.response_model(),
    response_description="Get coins info"
)
def coins_info(
        db: Session = Depends(get_db),
):
    try:
        from system_object import SystemObjectsService
        response_list = []
        system_object_sr = SystemObjectsService()
        coins = system_object_sr.coin.find_item_multi(db=db)

        for coin in coins:
            response_list.append(
                {
                    'name': coin.name,
                    "balance_in_tmn": coin.price_in_rial / 10,
                    "balance_in_usdt": round(coin.price_in_usdt, 2),
                    "symbol": coin.symbol,
                    'logo_address': coin.logo_address,
                    'name_fa': coin.fa_name,
                    'networks': list(coin.networks.values())
                }
            )

        coin_info_RM.status_code(200)
        return coin_info_RM.response(response_list)
    except Exception as e:
        return coin_info_RM.exception(e)
