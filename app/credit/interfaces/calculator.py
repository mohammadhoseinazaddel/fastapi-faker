from sqlalchemy.orm import Session

from order import OrderService
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.config import settings
from system_object import SystemObjectsService
from user_assets import UserAssetsService
from ..api.v1.schemas.credit_admin import CqGetCreditDetails
from ..models.calculator import credit_calculator_crud, CrdCalculator
from ..models.schemas.calculator import CalculatorCreateSchema, CalculatorUpdateSchema, CalculatorGetMulti


class CalculatorInterface(InterfaceBase):

    def __init__(
            self,
            crud: CRUDBase,
            create_schema,
            update_schema,
            get_multi_schema
    ):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = credit_calculator_crud

    def calculate_credit(
            self,
            db: Session,
            user_id: int,
            input_type: str = None,
            input_unique_id: int = None
    ) -> CrdCalculator:

        from .user_credit import credit_user_agent
        system_object_sr = SystemObjectsService()
        user_asset_sr = UserAssetsService()
        order_sr = OrderService()

        credit = credit_user_agent.find_item_multi(db=db, raise_not_found_exception=False, user_id=user_id)
        if credit:
            credit = credit[0]
            # if credit.is_locked:
            #     raise CreditIsLocked
        else:
            credit = credit_user_agent.add_item(db=db, user_id=user_id)

        non_free_credit = 0
        non_free_credit_used = 0
        free_credit = settings.BASE_FREE_CREDIT
        free_credit_used = 0

        user_asset_json = {
            "wallex": {},
            "wallpay": {},
        }

        # cs = score_agent.user_credit_score(db=db, user_id=user_id)
        cs = 1

        wallex_user_asset = user_asset_sr.wallex.get_user_asset(db=db, user_id=user_id)

        # get system coins
        wallpay_coins = system_object_sr.coin.find_item_multi(db=db)

        # sum of non-free-credit based on ltv and cs
        for coin in wallpay_coins:
            """
                disabled all collateral system in order process
            """
            # wallpay_balance = user_asset_sr.crypto_transaction.get_balance(db=db, user_id=user_id,
            # coin_name=coin.name)
            wallpay_balance = 0

            balance_in_rial = coin.price_in_rial * wallpay_balance
            balance_in_usdt = coin.price_in_usdt * wallpay_balance

            user_asset_json['wallpay'].update(
                {
                    'name': coin.name,
                    'balance': wallpay_balance,
                    'balance_in_rial': balance_in_rial,
                    'balance_in_usdt': balance_in_usdt,
                    'ltv': coin.ltv,
                }
            )

            non_free_credit += int(coin.ltv * cs * balance_in_rial)

            if wallex_user_asset['asset_balance']:
                for asset in wallex_user_asset['asset_balance']:
                    if asset['symbol'] == coin.wallex_symbol:
                        wallex_balance = asset['available']
                        balance_in_rial = coin.price_in_rial * wallex_balance
                        balance_in_usdt = coin.price_in_usdt * wallex_balance

                        user_asset_json['wallex'].update(
                            {
                                'name': coin.name,
                                'balance': wallex_balance,
                                'balance_in_rial': balance_in_rial,
                                'balance_in_usdt': balance_in_usdt,
                                'ltv': coin.ltv,
                            }
                        )

                        non_free_credit += int(coin.ltv * cs * balance_in_rial)

        used_credit_dict = order_sr.fund.get_all_used_credit(db=db, user_id=user_id)

        # Calculate used credit amount
        free_credit_used = used_credit_dict['used_free_credit']
        non_free_credit_used = used_credit_dict['used_non_free_credit']

        if input_type and input_unique_id:
            return self.add_item(
                db=db,
                credit_id=credit.id,
                non_free_credit=non_free_credit,
                used_non_free_credit=non_free_credit_used,
                free_credit=free_credit,
                used_free_credit=free_credit_used,
                asset_json=user_asset_json,
                cs=cs,
                input_type=input_type,
                input_unique_id=input_unique_id
            )
        else:
            return self.add_item(
                db=db,
                credit_id=credit.id,
                non_free_credit=non_free_credit,
                used_non_free_credit=non_free_credit_used,
                free_credit=free_credit,
                used_free_credit=free_credit_used,
                asset_json=user_asset_json,
                cs=cs,
            )

    def get_user_credit_details(self, page_number: int, page_size: int, **kwargs):
        data = {'result': [], 'total_count': None}

        result = self.crud.get_user_all_credit_details(
            db=kwargs['db'],
            skip=(page_number - 1) * page_size,
            limit=page_size,
            **CqGetCreditDetails(**kwargs).dict()
        )
        query_result, total_count = result['query_result'], result['total_count']

        for credit_obj in query_result:
            available_credit = credit_obj.non_free_credit+credit_obj.free_credit
            used_credit = credit_obj.used_non_free_credit+credit_obj.used_free_credit
            data['result'].append(
                {
                    'user_id': credit_obj.credit_id,
                    'created_at': credit_obj.created_at,
                    'available_credit': available_credit,
                    'used_credit': used_credit,
                }
            )
        data['total_count'] = total_count
        return data

    def get_total_credit(self, db: Session, calculate_id: int) -> int:
        calculate_obj = self.find_item_multi(db=db, id=calculate_id)[0]
        total_credit = calculate_obj.free_credit + calculate_obj.non_free_credit - \
                       calculate_obj.used_free_credit
        return total_credit


credit_calculator_agent = CalculatorInterface(
    crud=credit_calculator_crud,
    create_schema=CalculatorCreateSchema,
    update_schema=CalculatorUpdateSchema,
    get_multi_schema=CalculatorGetMulti
)
