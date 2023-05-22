import copy
import datetime

from sqlalchemy.orm import Session

from system.base.interface import InterfaceBase
from system.config import settings
from system_object import SystemObjectsService
from ..exceptions import fund as fund_exceptions
from ..exceptions.fund import FundNotFound, NothingToRepay, CreditIsNotEnough
from ..models.fund import fund_crud, OrdFund
from ..models.schemas.fund import FundCreateSchema, FundGetMultiSchema, FundUpdateSchema


class FundInterface(InterfaceBase):
    system_object_SR = SystemObjectsService()
    from system.base.crud import CRUDBase

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema, exceptions):
        super().__init__(crud, create_schema, update_schema, get_multi_schema, exceptions)

    def make_fund(
            self,
            order_id: int,
            order_identifier: str,
            order_amount: int,
            order_type: str,
            free_credit: int,
            cs: int,
            user_id: int,
            db: Session
    ):
        used_free_credit = 0
        extra_pay = 0
        payment_amount = 0
        need_payment = False
        used_asset_json = {
            'wallpay': {},
            'wallex': {},
        }
        temp_fund_amount = order_amount

        while temp_fund_amount:
            if not free_credit:
                break
            if free_credit:
                if free_credit > temp_fund_amount:
                    free_credit -= temp_fund_amount
                    used_free_credit = copy.copy(temp_fund_amount)
                    temp_fund_amount = 0
                    continue
                if free_credit < temp_fund_amount:
                    temp_fund_amount -= free_credit
                    used_free_credit = copy.copy(free_credit)
                    free_credit = 0
                    continue
                if free_credit == temp_fund_amount:
                    used_free_credit = copy.copy(free_credit)
                    free_credit = temp_fund_amount = 0
                    continue

        created_fund = self.add_item(
            db=db,
            order_id=order_id,
            order_amount=order_amount,
            user_id=user_id,
            used_non_free_credit=0,
            used_free_credit=used_free_credit,
        )

        if temp_fund_amount:

            """
                disabled all collateral system in order process
            """
            # result_dict = self._estimate_maximum_wallpay_asset_to_block(
            #     user_id=user_id,
            #     max_rial_amount_to_block=temp_fund_amount,
            #     cs=cs,
            #     db=db
            # )
            # remain_rial_to_block = result_dict['remain_rial_amount_to_block']
            # if result_dict['used_wallpay_asset_in_rial'] > 0:
            #     used_asset_json['wallpay'] = result_dict['used_asset_json']
            #     created_fund.need_collateral = True
            #     created_fund.used_asset_json = used_asset_json
            #
            # if remain_rial_to_block:
            #
            #     result_dict = self._estimate_maximum_wallex_asset_to_block(
            #         user_id=user_id,
            #         max_rial_amount_to_block=remain_rial_to_block,
            #         cs=cs,
            #         db=db
            #     )
            #     remain_rial_to_block = result_dict['remain_rial_amount_to_block']
            #     if result_dict['used_wallex_asset_in_rial'] > 0:
            #         used_asset_json['wallex'] = result_dict['used_asset_json']
            #         created_fund.need_collateral = True
            #         created_fund.need_wallex_asset = True
            #         created_fund.used_asset_json = used_asset_json
            #
            #     if remain_rial_to_block:
            #         extra_pay = remain_rial_to_block

            extra_pay = temp_fund_amount

        created_fund.extra_money_to_pay = extra_pay

        if order_type == 'POST_PAY':
            payment_amount = extra_pay

        if order_type == "PAY_IN_FOUR":
            payment_amount = extra_pay + (order_amount - extra_pay) / 4
            payment_amount = int(payment_amount)

        if 0 < payment_amount < settings.MINIMUM_BANK_PAYMENT_AMOUNT:
            payment_amount = settings.MINIMUM_BANK_PAYMENT_AMOUNT

        created_fund.payment_amount = payment_amount

        if not created_fund.need_collateral:
            self.get_payment_id(
                db=db,
                order_identifier=order_identifier,
                fund=created_fund
            )

        self._calculate_update_fill_percentage(fund_id=created_fund.id, db=db)

        return {
            'need_collateral': created_fund.need_collateral,
            'need_payment': True if created_fund.payment_amount > 0 else False
        }

    # def create_debt_or_loans(
    #         self,
    #         fund_id: int,
    #         order_type: str,
    #         user_id: int,
    #         db: Session
    #
    # ):
    #     fund = self.find_item_multi(db=db, id=fund_id)[0]
    #
    #     if order_type == "POST_PAY":
    #         debt_agent.add_item(
    #             db=db,
    #             fund_id=fund.id,
    #             user_id=user_id,
    #             amount=fund.used_non_free_credit + fund.used_free_credit
    #         )
    #     if order_type == "PAY_IN_FOUR":
    #         for i in range(1, 5):
    #             created_loan = loan_agent.add_item(
    #                 db=db,
    #                 fund_id=fund_id,
    #                 loan_position=i,
    #                 amount=(fund.used_non_free_credit + fund.used_free_credit) / 4,
    #                 settlement_time=loan_agent.get_loan_settle_time(db=db, loan_position=i),
    #                 user_id=user_id,
    #             )
    #             if i == 1:
    #                 self.confirm_repay(
    #                     db=db,
    #                     debt_ids=[],
    #                     loan_ids=[created_loan.id]
    #                 )

    def get_all_used_credit(self, db: Session, user_id: int) -> dict:
        used_free_credit = 0
        used_non_free_credit = 0
        funds = self.find_item_multi(
            db=db,
            user_id=user_id,
            raise_not_found_exception=False,
            completely_repaid_at__isnull=True
        )

        for fund in funds:
            used_free_credit += fund.used_free_credit - fund.repaid_free_credit
            used_non_free_credit = fund.used_non_free_credit - fund.repaid_non_free_credit

        return {
            "used_free_credit": used_free_credit,
            "used_non_free_credit": used_non_free_credit
        }

    # def get_all_fund_detail_to_repay(self, db: Session, user_id: int):
    #     from order.models.pay import OrdPay
    #     from system_object import SystemObjectsService
    #     from .debt import debt_agent
    #     from .loan import loan_agent
    #     from .pay import pay_agent
    #
    #     system_object_sr = SystemObjectsService()
    #
    #     fund_model = self.crud.model
    #
    #     result = db.query(fund_model, OrdPay.type, OrdPay.title, OrdPay.merchant_id, OrdPay.amount).filter(
    #         fund_model.order_id == OrdPay.id,
    #         fund_model.deleted_at == None,
    #         OrdPay.deleted_at == None,
    #         OrdPay.status == pay_agent.crud.STATUS_SUCCESS,
    #         fund_model.completely_repaid_at == None,
    #         OrdPay.user_id == user_id
    #     ).all()
    #
    #     response_list = []
    #     for item in result:
    #         fund_obj = item[0]
    #         order_type = item[1]
    #         order_title = item[2]
    #         merchant_id = int(item[3])
    #         order_price = int(item[4])
    #
    #         total_remain_debt = 0
    #         to_pay = 0
    #         settle_time = None
    #         merchant = system_object_sr.merchant.find_item_multi(db=db, id=merchant_id)[0]
    #         merchant_logo_address = merchant.logo_address
    #         merchant_logo_background = merchant.logo_background_color
    #         merchant_name_fa = merchant.name_fa
    #
    #         if order_type == 'POST_PAY':
    #             debt = debt_agent.find_item_multi(db=db, fund_id=fund_obj.id)[0]
    #             total_remain_debt += debt.amount
    #             settle_time = debt.settlement_time
    #             if self._can_repay_or_not(settle_time):
    #                 to_pay = debt.amount
    #         if order_type == "PAY_IN_FOUR":
    #             loans = loan_agent.find_item_multi(
    #                 db=db,
    #                 fund_id=fund_obj.id,
    #                 order_by=('loan_position', 'asc'),
    #                 paid_at__isnull=True
    #             )
    #             settle_time = loans[0].settlement_time
    #             for loan in loans:
    #                 total_remain_debt += loan.amount
    #                 if self._can_repay_or_not(loan.settlement_time):
    #                     to_pay += loan.amount
    #
    #         response_list.append({
    #             'id': fund_obj.id,
    #             'order_price': order_price,
    #             'title': order_title,
    #             'order_type': order_type,
    #             'total_remain_debt': total_remain_debt / 10,
    #             'to_pay': to_pay / 10,
    #             'settle_time': settle_time,
    #             'merchant_logo_address': merchant_logo_address,
    #             'merchant_logo_background_color': merchant_logo_background,
    #             'merchant_name_fa': merchant_name_fa
    #         })
    #
    #     return response_list

    def repay(self, list_of_fund_id: list, db: Session, user_id: int):
        # TODO: we should rewrite this method
        from order import OrderService
        from finance import FinanceService

        order_sr = OrderService()
        finance_sr = FinanceService()
        payment_detail_list = []
        for fund_id in list_of_fund_id:
            fund = self.find_item_multi(db=db, id=fund_id, user_id=user_id)[0]
            order = order_sr.pay.find_item_multi(db=db, id=fund.order_id)[0]

            if order.type == "POST_PAY":
                debt = order_sr.debt.find_item_multi(db=db, fund_id=fund_id)[0]
                if self._can_repay_or_not(debt.settlement_time):
                    payment_detail_list.append(
                        {
                            'amount': debt.amount,
                            'input_type': 'debt',
                            'input_unique_id': debt.id,
                            'ord_order_uuid': order.identifier
                        }
                    )
            if order.type == "PAY_IN_FOUR":
                loans = order_sr.loan.find_item_multi(db=db, fund_id=fund_id)
                for loan in loans:
                    if loan.paid_at:
                        continue
                    if self._can_repay_or_not(loan.settlement_time):
                        payment_detail_list.append(
                            {
                                'amount': loan.amount,
                                'input_type': 'loan',
                                'input_unique_id': loan.id,
                                'ord_order_uuid': order.identifier
                            }
                        )
        if not payment_detail_list:
            raise NothingToRepay
        pay_obj = finance_sr.bank_pay.create_repay_pay_order_bank_pay_for_multiple_order(
            db=db,
            bank_pay_detail=payment_detail_list,
            user_id=user_id,
        )

        payment_redirect_url = finance_sr.payment_gateway.send_to_payment_gateway(
            bank_payment_id=pay_obj.id,
            db=db
        )['psp_switching_url']
        return {
            'redirect_url': payment_redirect_url,
            'total_amount': pay_obj.amount
        }

    def repay_free_credit_from_refund(self, order_id: int, db: Session, user_id: int, repay_amount: int):
        from order import OrderService
        order_sr = OrderService()

        fund_obj = order_sr.fund.find_item_multi(db=db, order_id=order_id, user_id=user_id, return_first_obj=True)
        if repay_amount + fund_obj.repaid_free_credit > fund_obj.used_free_credit:
            raise SystemError("repay_amount can't be less than used_free_credit")
        fund_obj.repaid_free_credit = fund_obj.repaid_free_credit + repay_amount


    # def confirm_repay(self, db: Session, debt_ids: list, loan_ids: list):
    #     from .debt import debt_agent
    #     from .loan import loan_agent
    #
    #     for debt_id in debt_ids:
    #         debt = debt_agent.find_item_multi(db=db, id=debt_id)[0]
    #         fund = self.find_item_multi(db=db, id=debt.fund_id)[0]
    #
    #         # update fund
    #         self.update_item(
    #             db=db,
    #             find_by={'id': fund.id},
    #             update_to={
    #                 'completely_repaid_at': datetime.datetime.now(),
    #                 'repaid_free_credit': fund.used_free_credit,
    #                 'repaid_non_free_credit': fund.used_non_free_credit,
    #             }
    #         )
    #
    #         # update debt paid_at
    #         debt_agent.update_item(db=db, find_by={'id': debt_id}, update_to={'paid_at': datetime.datetime.now()})
    #
    #     for loan_id in loan_ids:
    #         loan = loan_agent.find_item_multi(db=db, id=loan_id)[0]
    #         fund = self.find_item_multi(db=db, id=loan.fund_id)[0]
    #
    #         # update loan paid_at
    #         loan_agent.update_item(db=db, find_by={'id': loan_id}, update_to={'paid_at': datetime.datetime.now()})
    #
    #         used_free_credit = copy.copy(fund.used_free_credit)
    #         repaid_free_credit = copy.copy(fund.repaid_free_credit)
    #
    #         used_non_free_credit = copy.copy(fund.used_non_free_credit)
    #         repaid_non_free_credit = copy.copy(fund.used_non_free_credit)
    #
    #         temp_amount = loan.amount
    #         while temp_amount:
    #             if used_free_credit - repaid_free_credit > 0:
    #                 if used_free_credit - repaid_free_credit >= loan.amount:
    #                     repaid_free_credit += loan.amount
    #                     temp_amount = 0
    #                     continue
    #                 else:
    #                     free = used_free_credit - repaid_free_credit
    #                     temp_amount -= free
    #                     repaid_free_credit += free
    #                     continue
    #             if used_non_free_credit - repaid_non_free_credit > 0:
    #                 if used_non_free_credit - repaid_non_free_credit >= loan.amount:
    #                     repaid_free_credit += loan.amount
    #                     temp_amount = 0
    #                     continue
    #                 else:
    #                     raise CreditIsNotEnough
    #
    #         # update fund to
    #         self.update_item(
    #             db=db,
    #             find_by={'id': fund.id},
    #             update_to={
    #                 'repaid_free_credit': repaid_free_credit,
    #                 'repaid_non_free_credit': repaid_non_free_credit,
    #             }
    #         )
    #
    #         if loan.loan_position == 4:  # it means fund completely repaid
    #
    #             # update fund
    #             self.update_item(
    #                 db=db,
    #                 find_by={'id': loan.fund_id},
    #                 update_to={
    #                     'completely_repaid_at': datetime.datetime.now(),
    #                 }
    #             )

    @staticmethod
    def _can_repay_or_not(settle_time: datetime) -> bool:
        if datetime.datetime.now() >= (settle_time - datetime.timedelta(days=5)):
            return True

    def _estimate_maximum_wallpay_asset_to_block(
            self,
            user_id: int,
            max_rial_amount_to_block: int,
            cs: float,
            db: Session,
    ) -> dict:
        """
            This method block user asset just based on assets that user has in Wallpay
            Block assets with order -> order by asset ltv descending
            result_dict = {
                'remain_rial_amount_to_block': 0,
                'used_asset_json':[
                    {'currency':'bitcoin', 'amount':0.001, 'coin_price_in_rial':650000, 'balance_collateral':0}
                ]
            }
        """
        from system_object import SystemObjectsService
        from user_assets import UserAssetsService

        system_object_sr = SystemObjectsService()
        user_assets_sr = UserAssetsService()

        remain_rial_amount_to_block = max_rial_amount_to_block

        block_list = []

        db_coins_list_order_by_ltv_desc = system_object_sr.coin.find_item_multi(db=db, order_by=('ltv', 'desc'))

        # block asset in wallpay first
        for coin in db_coins_list_order_by_ltv_desc:
            balance = user_assets_sr.crypto_transaction.get_balance(db=db, user_id=user_id, coin_name=coin.name)
            # check wallet balance shouldn't be 0
            if not balance:
                continue

            balance_can_be_collateral = balance * coin.ltv * coin.price_in_rial * (1 / cs)

            # This is termination expression -> when remain_rial amount is 0 we will return
            if remain_rial_amount_to_block:
                x = remain_rial_amount_to_block - balance_can_be_collateral

                create_result = self._create_asset_block_list(
                    x=x,
                    remain_rial_amount_to_block=remain_rial_amount_to_block,
                    block_list=block_list,
                    balance=balance,
                    balance_can_be_collateral=balance_can_be_collateral,
                    coin_price_in_rial=coin.price_in_rial,
                    coin_name=coin.name,
                    ltv=coin.ltv,
                )
                block_list = create_result['block_list']
                remain_rial_amount_to_block = create_result['remain_rial_amount_to_block']
                continue
            else:
                block_list.append(
                    {
                        'total_balance': balance,
                        'used_balance': 0,

                        'total_balance_in_rial': balance_can_be_collateral,
                        'used_balance_in_rial': 0,

                        'currency': coin.name,
                        'ltv': coin.ltv,
                        'coin_price_in_rial': coin.price_in_rial,
                    }
                )

        used_wallpay_asset_in_rial = 0
        if max_rial_amount_to_block > remain_rial_amount_to_block:
            used_wallpay_asset_in_rial = max_rial_amount_to_block - remain_rial_amount_to_block

        return {
            "used_wallpay_asset_in_rial": used_wallpay_asset_in_rial,
            'remain_rial_amount_to_block': remain_rial_amount_to_block,
            'used_asset_json': block_list
        }

    def _estimate_maximum_wallex_asset_to_block(
            self,
            user_id: int,
            max_rial_amount_to_block,
            cs: float,

            db: Session
    ) -> dict:
        from user_assets import UserAssetsService
        from system_object import SystemObjectsService
        user_assets_sr = UserAssetsService()
        system_object_sr = SystemObjectsService()

        wallex_detail_dict = user_assets_sr.wallex.get_user_asset(db=db, user_id=user_id, use_cache=False)
        remain_rial_amount_to_block = max_rial_amount_to_block
        wallex_assets = wallex_detail_dict['asset_balance']
        used_wallex_asset_in_rial = 0

        if not wallex_detail_dict['wallex_user_id']:
            return {
                "used_wallex_asset_in_rial": used_wallex_asset_in_rial,
                'remain_rial_amount_to_block': remain_rial_amount_to_block
            }

        db_coins_list_order_by_ltv_desc = system_object_sr.coin.find_item_multi(db=db, order_by=('ltv', 'desc'))
        block_list = []
        for coin in db_coins_list_order_by_ltv_desc:
            # This is termination expression -> when remain_rial amount is 0 we will return
            if remain_rial_amount_to_block:
                for wallex_asset in wallex_assets:
                    if wallex_asset['symbol'] == coin.wallex_symbol and wallex_asset['available']:
                        balance = wallex_asset['available']
                        balance_can_be_collateral = balance * coin.ltv * coin.price_in_rial * (1 / cs)

                        x = remain_rial_amount_to_block - balance_can_be_collateral

                        create_result = self._create_asset_block_list(
                            x=x,
                            remain_rial_amount_to_block=remain_rial_amount_to_block,
                            block_list=block_list,
                            balance=balance,
                            balance_can_be_collateral=balance_can_be_collateral,
                            coin_price_in_rial=coin.price_in_rial,
                            coin_name=coin.name,
                            ltv=coin.ltv,
                            wallex_symbol=wallex_asset['symbol'],
                        )
                        block_list = create_result['block_list']
                        remain_rial_amount_to_block = create_result['remain_rial_amount_to_block']
                        continue
            else:
                for wallex_asset in wallex_assets:
                    if wallex_asset['symbol'] == coin.wallex_symbol and wallex_asset['available']:
                        balance = wallex_asset['available']
                        balance_can_be_collateral = balance * coin.ltv * coin.price_in_rial * (1 / cs)

                        block_list.append({
                            'total_balance': balance,
                            'used_balance': 0,

                            'total_balance_in_rial': balance_can_be_collateral,
                            'used_balance_in_rial': 0,

                            'currency': coin.name,
                            'ltv': coin.ltv,
                            'wallex_symbol': wallex_asset['symbol'],
                            'coin_price_in_rial': coin.price_in_rial,
                        })

        if max_rial_amount_to_block > remain_rial_amount_to_block:
            used_wallex_asset_in_rial = max_rial_amount_to_block - remain_rial_amount_to_block

        return {
            "used_wallex_asset_in_rial": used_wallex_asset_in_rial,
            'remain_rial_amount_to_block': remain_rial_amount_to_block,
            'used_asset_json': block_list
        }

    def _calculate_update_fill_percentage(self, fund_id: int, db: Session, just_calculate: bool = False) -> int:
        fund = self.find_item_multi(db=db, id=fund_id)[0]
        used_free_credit = fund.used_free_credit
        used_non_free_credit = fund.used_non_free_credit
        extra_money_to_pay = fund.extra_money_to_pay
        order_amount = fund.order_amount
        percentage = 0

        fill_amount = used_free_credit + used_non_free_credit + extra_money_to_pay

        percentage = (fill_amount * 100) / order_amount

        self.update_item(db=db, find_by={'id': fund_id}, update_to={"fill_percentage": percentage})
        return percentage

    def get_payment_id(
            self,
            db: Session,
            order_identifier: str,
            fund: OrdFund
    ):
        from finance import FinanceService

        finance_sr = FinanceService()

        if fund.payment_amount > 0:

            bank_pay = finance_sr.bank.payment.add_item(
                db=db,
                input_type='pay_order',
                input_unique_id=fund.order_id,
                user_id=fund.user_id,
                amount=fund.payment_amount,
            )
            self.update_item(
                db=db,
                find_by={'id': fund.id},
                update_to={
                    'payment_amount': fund.payment_amount,
                    'payment_id': bank_pay.id
                }
            )

    def cancel_fund_process(self, db: Session, order_id: int, user_id: int):
        fund = self.find_item_multi(db=db, order_id=order_id)[0]

        from user_assets import UserAssetsService
        user_assets_sr = UserAssetsService()

        # unblock assets
        if fund.need_collateral:

            # unblock wallex assets
            if fund.need_wallex_asset:
                user_assets_sr.wallex.cancel_wallex_pay_request(
                    db=db,
                    token=fund.wallex_block_request_id,
                    user_id=fund.user_id,
                    input_type='fund',
                    input_unique_id=fund.id
                )

            # unblock wallpay assets
            result = user_assets_sr.crypto_transaction.find_blocked_coins(
                db=db,
                input_type='fund',
                input_unique_id=fund.id
            )
            for coin_name, balance in result.items():
                if balance:
                    user_assets_sr.crypto_transaction.unblock_balance(
                        user_id=user_id,
                        coin_name=coin_name,
                        input_type='fund',
                        input_unique_id=fund.id,
                        amount=balance,
                        db=db
                    )

        # soft delete fund
        self.delete_item(db=db, find_by={'id': fund.id})

    @staticmethod
    def get_collateral(db: Session, fund: OrdFund):
        from system_object import SystemObjectsService
        system_object_sr = SystemObjectsService()

        if not fund.need_collateral:
            raise FundNotFound

        used_wallpay_asset_list = fund.used_asset_json['wallpay']
        used_wallex_asset_list = fund.used_asset_json['wallex']

        result_list = []

        coins = system_object_sr.coin.find_item_multi(db=db)
        for coin in coins:
            blocked_amount = 0
            blocked_amount_in_tmn = 0
            blocked_amount_in_tmn_max = 0
            risk_label = None
            for wallpay_asset_dict in used_wallpay_asset_list:
                if wallpay_asset_dict['currency'] == coin.name:
                    blocked_amount_in_tmn_max += wallpay_asset_dict['total_balance_in_rial']
                    blocked_amount += wallpay_asset_dict['used_balance']
                    blocked_amount_in_tmn += wallpay_asset_dict['used_balance_in_rial'] / 10

            for wallex_asset_dict in used_wallex_asset_list:
                if wallex_asset_dict['currency'] == coin.name:
                    blocked_amount_in_tmn_max += wallex_asset_dict['total_balance_in_rial']
                    blocked_amount += wallex_asset_dict['used_balance']
                    blocked_amount_in_tmn += wallex_asset_dict['used_balance_in_rial'] / 10

            if 0 <= coin.ltv <= 0.5:
                risk_label = 'High risk'
            elif 0.5 < coin.ltv <= 0.65:
                risk_label = 'Medium risk'
            elif 0.65 < coin.ltv:
                risk_label = 'Low risk'
            result_list.append({
                'coin_name_fa': coin.fa_name,
                'coin_symbol': coin.symbol,
                'coin_logo_address': coin.logo_address,
                'ltv': coin.ltv,
                'risk_label': risk_label,
                'blocked_amount': blocked_amount,
                'blocked_amount_in_tmn': blocked_amount_in_tmn,
                'blocked_amount_in_tmn_max': blocked_amount_in_tmn_max
            })
        return result_list

    @staticmethod
    def get_satisfy_percentage(
            asset_list: list,
            used_free_credit: int,
            order_amount: int
    ):
        percentage = 0

        blocked_amount_in_tmn_max = 0
        blocked_amount_in_tmn_total = 0

        for asset in asset_list:
            blocked_amount_in_tmn_max += asset['blocked_amount_in_tmn_max']
            blocked_amount_in_tmn_total += asset['blocked_amount_in_tmn']

        amount_need_collateral = (order_amount - used_free_credit)  # convert numbers to tmn

        if blocked_amount_in_tmn_max > amount_need_collateral:
            if blocked_amount_in_tmn_total > amount_need_collateral:
                percentage = 100 + (
                        (blocked_amount_in_tmn_max / (blocked_amount_in_tmn_total - amount_need_collateral)) * 10)
            else:
                percentage = amount_need_collateral / blocked_amount_in_tmn_total * 10

        if blocked_amount_in_tmn_max <= amount_need_collateral:
            percentage = (blocked_amount_in_tmn_max / blocked_amount_in_tmn_total) * 10

        return percentage

    def block_wallpay_asset_by_json(self, db: Session, fund: OrdFund):
        from user_assets import UserAssetsService
        user_assets_sr = UserAssetsService()

        used_non_free_credit = fund.used_non_free_credit

        wallpay_asset_list = fund.used_asset_json['wallpay']
        for asset in wallpay_asset_list:
            user_assets_sr.crypto_transaction.block_balance(
                user_id=fund.user_id,
                coin_name=asset['currency'],
                input_type='fund',
                input_unique_id=fund.id,
                amount=asset['used_balance'],
                db=db
            )
            used_non_free_credit += asset['used_balance_in_rial']

        self.update_item(db=db, find_by={'id': fund.id}, update_to={"used_non_free_credit": used_non_free_credit})
        self._calculate_update_fill_percentage(db=db, fund_id=fund.id)

    @staticmethod
    def _create_asset_block_list(
            x: int,
            remain_rial_amount_to_block: int,
            block_list: list,
            balance: int,
            balance_can_be_collateral: int,
            coin_price_in_rial: int,
            coin_name: str,
            ltv: int,
            wallex_symbol: str = '',

    ):
        if x == 0:
            block_list.append({
                'total_balance': balance,
                'used_balance': balance,

                'total_balance_in_rial': balance_can_be_collateral,
                'used_balance_in_rial': balance_can_be_collateral,

                'currency': coin_name,
                'wallex_symbol': wallex_symbol,
                'ltv': ltv,
                'coin_price_in_rial': coin_price_in_rial
            })
            remain_rial_amount_to_block = 0
        if x > 0:
            block_list.append({
                'total_balance': balance,
                'used_balance': balance,

                'total_balance_in_rial': balance_can_be_collateral,
                'used_balance_in_rial': balance_can_be_collateral,

                'currency': coin_name,
                'ltv': ltv,
                'wallex_symbol': wallex_symbol,
                'coin_price_in_rial': coin_price_in_rial,
            })
            remain_rial_amount_to_block -= balance * coin_price_in_rial * ltv
        if x < 0:
            alpha = remain_rial_amount_to_block / balance_can_be_collateral
            amount_to_block = balance * alpha
            used_balance_in_rial = amount_to_block * coin_price_in_rial * ltv

            if 0 < remain_rial_amount_to_block - used_balance_in_rial < 2:
                used_balance_in_rial = remain_rial_amount_to_block

            block_list.append({
                'total_balance': balance,
                'used_balance': amount_to_block,

                'total_balance_in_rial': balance_can_be_collateral,
                'used_balance_in_rial': used_balance_in_rial,

                'currency': coin_name,
                'ltv': ltv,
                'wallex_symbol': wallex_symbol,
                'coin_price_in_rial': coin_price_in_rial,
            })
            remain_rial_amount_to_block = 0
        return {
            'remain_rial_amount_to_block': remain_rial_amount_to_block,
            'block_list': block_list
        }

    def create_wallex_block_request(self, db: Session, fund: OrdFund, order_uuid: str):
        from user_assets import UserAssetsService

        user_assets_sr = UserAssetsService()

        used_wallex_asset_list = fund.used_asset_json['wallex']
        request_block_id = user_assets_sr.wallex.order_request_block_asset(
            db=db,
            block_asset=used_wallex_asset_list,
            user_id=fund.user_id,
            input_type='fund',
            input_unique_id=fund.id,
            order_uuid=order_uuid,
            callback_type='pay-order'
        )
        self.update_item(
            db=db,
            find_by={'id': fund.id},
            update_to={'wallex_block_request_id': request_block_id}
        )

    def block_wallex_asset_by_json(self, db: Session, fund: OrdFund):
        used_non_free_credit = fund.used_non_free_credit

        wallex_asset_list = fund.used_asset_json['wallex']
        for asset in wallex_asset_list:
            used_non_free_credit += asset['used_balance_in_rial']

        self.update_item(db=db, find_by={'id': fund.id}, update_to={"used_non_free_credit": used_non_free_credit})
        self._calculate_update_fill_percentage(db=db, fund_id=fund.id)


fund_agent = FundInterface(
    crud=fund_crud,
    create_schema=FundCreateSchema,
    update_schema=FundUpdateSchema,
    get_multi_schema=FundGetMultiSchema,
    exceptions=fund_exceptions
)
