from sqlalchemy.orm import Session

from system.base.mixins import InterfaceLifeCycle
from system.dbs.postgre import SessionLocal


class SettleInterface(InterfaceLifeCycle):
    def __init__(self):
        from .settle_pgw import settle_pgw_agent
        from .settle_credit import settle_credit_agent
        from .transfer import transfer_agent

        self.pgw = settle_pgw_agent
        self.credit = settle_credit_agent
        self.transfer = transfer_agent

    def order_manager(
            self,
            merchant_id: int,
            user_id: int,
            order_id: int,
            order_uuid: str,
            order_status: str,
            used_credit: int,
            extra_payment_amount: int,
            commission_id: int,
            db: Session = SessionLocal()
    ):
        from .debt_user import debt_user_agent
        from order.interfaces.commission import commission_agent

        if order_status == 'SUCCESS':
            #  رکورد بستانکاری مرچنت برای مقدار پرداختی درگاه
            settle_pgw_rec = self.pgw.find_item_multi(
                db=db,
                order_id=order_id,
                type='pay',
                raise_not_found_exception=False
            )
            if settle_pgw_rec:
                raise SystemError('order settle pgw was registered before')

            settle_pgw_rec = self.pgw.add_item(
                db=db,
                order_id=order_id,
                order_uuid=order_uuid,
                type='pay',
                merchant_id=merchant_id,
                amount=extra_payment_amount - commission_agent.get_pgw_commission_plus_fee(
                    pgw_amount=extra_payment_amount,
                    commission_id=commission_id,
                    db=db
                )
            )

            #  رکورد بستانکاری مرچنت برای مقدار کردیت داده شده
            settle_credit_rec = self.credit.find_item_multi(
                db=db,
                order_id=order_id,
                type='pay',
                raise_not_found_exception=False
            )
            if settle_credit_rec:
                raise SystemError('order settle pgw was registered before')

            settle_credit_rec = self.credit.add_item(
                db=db,
                order_id=order_id,
                order_uuid=order_uuid,
                type='pay',
                merchant_id=merchant_id,
                amount=used_credit - commission_agent.get_credit_commission(
                    used_credit=used_credit,
                    commission_id=commission_id,
                    db=db
                )
            )

            # رکورد بدهی کاربر
            debt_user_agent.add_item(
                db=db,
                user_id=user_id,
                amount=used_credit,
                due_date=debt_user_agent.get_due_date(),
                input_type='OrdPay',
                order_id=order_id,
                input_unique_id=order_id
            )

    def get_settle_credit_pwg(self, page_number: int, page_size: int, **kwargs):
        data = {'result': [], 'total_count': None}
        credit_data = dict()
        pgw_data = dict()
        data_count = 0
        settlement_type = kwargs['settlement_type']
        # 'ALL', 'CREDIT', 'PGW'
        if settlement_type in ['all', 'ALL', 'credit']:
            credit_data = self.credit.get_settle_credit(page_number=page_number, page_size=page_size, **kwargs)
        if settlement_type in ['all', 'ALL', 'pgw']:
            pgw_data = self.pgw.get_settle_pgw(page_number=page_number, page_size=page_size, **kwargs)
        if credit_data:
            for credit_result in credit_data.get('result'):
                data['result'].append(credit_result)
            data_count += credit_data.get('total_count')
        if pgw_data:
            for pgw_result in pgw_data.get('result'):
                data['result'].append(pgw_result)
            data_count += pgw_data.get('total_count')
        if data_count > 0:
            data['total_count'] = data_count
        return data


settle_agent = SettleInterface()
