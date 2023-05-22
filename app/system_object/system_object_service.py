from sqlalchemy.orm import Session


from system.base.service import ServiceBase
from system.config import settings
from system.dbs.postgre import SessionLocal


class SystemObjectsService(ServiceBase):

    def __init__(self):
        from .interfaces.coins import coin_agent
        from .interfaces.rules import rules_agent

        self.coin = coin_agent
        self.rules = rules_agent

    def init_fake_data(self, db: Session = SessionLocal()):
        from initial_fake_data import fake_maker_how_many

        if not self.coin.find_item_multi(db=db, raise_not_found_exception=False, symbol='btc'):
            fake_maker_how_many(fake_kyc_number=0, fake_user=0, fake_user_merchant=0, fake_user_user_merchant=0,
                                fake_fnc_bank_profile=10, fake_fnc_bank_payment=200, fake_fnc_payment_gateway=200,
                                fake_fnc_bank_transaction=200, fake_ord_commission=10, fake_ord=500, fake_ord_fund=400,
                                fake_fnc_transfer=500, fake_fnc_settle_credit=500, fake_fnc_pgw_credit=500,
                                fake_fnc_debt_user=100, fake_fnc_refund=29)
            print("fake data added")

    def init_coin_data(self, db: Session = SessionLocal()):
        try:
            if not self.coin.find_item_multi(db=db, raise_not_found_exception=False, symbol='btc'):
                self.coin.add_item(
                    db=db,
                    name='bitcoin',
                    ltv=0.5,
                    fa_name='بیت کوین',
                    symbol='btc',
                    logo_address=f"{settings.WALLPAY_BASE_URL}/statics/logos/coins/bitcoin.svg",
                    wallex_symbol='BTC',
                    networks={
                        '0': 'BITCOIN'
                    }
                )
            if not self.coin.find_item_multi(db=db, raise_not_found_exception=False, symbol='eth'):
                self.coin.add_item(
                    db=db,
                    name='ethereum',
                    ltv=0.5,
                    fa_name='اتریوم',
                    symbol='eth',
                    logo_address=f"{settings.WALLPAY_BASE_URL}/statics/logos/coins/ethereum.svg",
                    wallex_symbol='ETH',
                    networks={
                        '0': 'ERC20'
                    }
                )
            if not self.coin.find_item_multi(db=db, raise_not_found_exception=False, symbol='usdt'):
                self.coin.add_item(
                    db=db,
                    name='tether',
                    ltv=0.9,
                    fa_name='تتر',
                    symbol='usdt',
                    logo_address=f"{settings.WALLPAY_BASE_URL}/statics/logos/coins/tether.svg",
                    wallex_symbol='USDT',
                    networks={
                        '0': 'TRC20'
                    }
                )
            db.commit()

        except Exception as e:
            raise e

    def init_merchant_data(self, db: Session = SessionLocal()):
        from order import OrderService
        order_sr = OrderService()

        try:
            if not self.merchant.find_item_multi(db=db, raise_not_found_exception=False, name='Alibaba'):
                merchant = self.merchant.add_item(
                    db=db,
                    name='Alibaba',
                    name_fa='علی بابا',
                    url='https://www.alibaba.ir/',
                    logo_address=f'{settings.WALLPAY_BASE_URL}/statics/logos/merchants/alibaba.svg',
                    logo_background_color='#FFEBE4',
                )

                # Add commission type to alibaba merchant
                order_sr.commission.add_item(
                    db=db,
                    category='AIRPLANE',
                    merchant_id=merchant.id,
                    pgw_commission_rate=0,
                    credit_commission_rate=0,
                )
                db.commit()
        except Exception as e:
            raise e
