from typing import List

from pydantic import BaseModel, Field


class CoinInfoResponse(BaseModel):
    name: str = \
        Field(...,
              title='asset-name',
              description='Name of asset',
              example='بیت کوین',
              )

    balance_in_tmn: int = \
        Field(...,
              title='asset balance in tmn',
              description='Balance in tmn',
              example=675000000,
              )

    balance_in_usdt: float = \
        Field(...,
              title='balance in usdt',
              description='Balance price in usdt',
              example=125.34,
              )

    symbol: str = \
        Field(...,
              title='asset symbol',
              description='Symbol of asset',
              example="BTC",
              )
    logo_address: str = \
        Field(...,
              title='logo-address',
              description='Address of logo',
              example='http://localhost:8000/logos/alibaba.svg',
              )
    name_fa: str = \
        Field(...,
              title='asset-fa-name',
              description='Persian name of asset',
              example='بیت کوین',
              )
    networks: List[str]
