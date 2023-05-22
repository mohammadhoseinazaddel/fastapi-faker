from pydantic import BaseModel, Field


class UserAssetEstimateResponse(BaseModel):
    name: str = \
        Field(...,
              title='asset-name',
              description='Name of asset',
              example='بیت کوین',
              )
    balance: float = \
        Field(...,
              title='asset-balance',
              description='Coin asset balance',
              example=1.002,
              )

    total_balance: float = \
        Field(...,
              title='total-balance',
              description='total balance of user',
              example=2.002,
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
    coin_price_usdt: float = \
        Field(...,
              title='usdt-coin-price',
              description='Coin price in usdt',
              example=110.21,
              )
    coin_price_tmn: int = \
        Field(...,
              title='coin-price-tmn',
              description='Coin price in tmn',
              example=650000000,
              )

    froze_balance: float = \
        Field(...,
              title='froze balance',
              description='froze amount',
              example=0.02,
              )


class UserAssetListResponse(BaseModel):
    # TODO fix this response for farzad and change to it to schema in schema
    user_asset: list = Field(...,
                             title='User asset list',
                             description='return list of user asset list',
                             example={
                                 "user_asset": [
                                     {
                                         "tmn": {
                                             "amount": 3000000,
                                             "tmn_amount": 3000000
                                         }
                                     },
                                     {
                                         "bitcoin": {
                                             "amount": 1.002000,
                                             "tmn_amount": 664616525
                                         }
                                     }
                                 ]
                             }
                             )


class DepositAddressRequest(BaseModel):
    coin_name: str = \
        Field(...,
              min_length=3,
              max_length=12,
              title='Coin Name',
              description='Requested address coin name',
              example='BITCOIN',
              )
    network_name: str = \
        Field(...,
              min_length=3,
              max_length=8,
              title='Network Name',
              description='Requested address network name',
              example='TRC20',
              )


class DepositAddressResponse(BaseModel):
    address: str = \
        Field(...,
              min_length=3,
              title='Address',
              description='Requested address',
              example='1A5kGMxoZXBQXYbwoAVBrcs9mE9ecCkpWE',
              )


class VerifyAddressRequest(BaseModel):
    address: str = \
        Field(...,
              min_length=3,
              title='Address',
              description='Requested address',
              example='1A5kGMxoZXBQXYbwoAVBrcs9mE9ecCkpWE',
              )


class VerifyAddressResponse(VerifyAddressRequest):
    is_valid: bool = \
        Field(...,
              title='Is Valid',
              description='You Can Find Given Address is Verified or Not',
              example=True
              )


class WithdrawRequest(BaseModel):
    coin: str = \
        Field(...,
              min_length=3,
              max_length=12,
              title='coin name',
              description='coin names',
              example='bitcoin',
              )
    network: str = \
        Field(...,
              min_length=3,
              max_length=12,
              title='network name',
              description='network names',
              example='BITCOIN',
              )
    address: str = \
        Field(...,
              min_length=3,
              title='Address',
              description='withdraw destination address',
              example='1MSyApyYxSX3BDKHYw56CSySFw59tbESZv',
              )
    memo: str = \
        Field(...,
              title='memo',
              description='withdraw destination memo',
              example='875654653',
              )
    amount: float = \
        Field(...,
              title='amount',
              description='Withdraw Amount',
              example=0.045,
              )


class WithdrawResponse(BaseModel):
    trace_id: str = \
        Field(...,
              min_length=3,
              title='Withdraw Trace Id',
              description='Withdraw Trace Id',
              example='alifg98y-sldvjbk-sdkvjb-sdkjvb',
              )
