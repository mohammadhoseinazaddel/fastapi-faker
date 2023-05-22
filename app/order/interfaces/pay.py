import datetime

from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.config import settings
from system.dbs.postgre import SessionLocal
from system_object import SystemObjectsService
from ..api.v1.schemas.order_admin import CqGetOrderDetails, CqGetUserOrders
from ..exceptions.pay import OrderHasBeenExpired, OrderIsNotAuthenticate, OrderIsProcessing

from finance.models.settle_credit import FncSettleCredit
from finance.models.settle_pgw import FncSettlePgw

# under develop
# from ..exceptions.pay import OrderActionNotSupported, OrderActionTimeExpired, OrderActionIsNotUnverified, OrderStatusNotSuccess

# this lines should be removed and code logic change
# keep and use this approach for time issue
from ..models.pay import pay_crud, OrdPay
from ..models.order import order_crud
from ..models.schemas.pay import GetMultiOrdPay, CreatePayOrderSchema, UpdatePayOrder
from ..api.v1.schemas.order_merchant import OrderGetSchema
from ..api.v1.schemas.order_merchant import OrderMerchantResponse, OrderCommission


class PayOrderInterface(InterfaceBase):
    system_object_SR = SystemObjectsService()

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        from ..exceptions import pay as pay_exception
        from ..interfaces.fund import fund_agent
        self.crud = pay_crud
        self.model = OrdPay
        self.exception = pay_exception
        self.fund = fund_agent

    def check_order_validity(self, db: Session, uuid: str):

        from order import OrderService
        order_sr = OrderService()
        record = order_sr.pay.find_item_multi(db=db, identifier=uuid)[0]

        diff = (datetime.datetime.now() - record.created_at).seconds / 60
        if int(diff) > settings.ORDER_EXPIRATION_TIME:
            raise OrderHasBeenExpired
        return record

    async def register_order_to_user(self, db: Session, user_id: int, uuid: str):
        record = self.find_item_multi(db=db, identifier=uuid)[0]
        if record.user_id is None:
            record.user_id = user_id
            db.commit()
        else:
            raise OrderIsProcessing

    @staticmethod
    def check_order_user_validity(record: OrdPay, user_id):
        if record.user_id is not user_id:
            raise OrderIsNotAuthenticate

    def finish_expired_orders(self):
        db = SessionLocal()
        records = self.find_item_multi(
            db=db,
            created_at__lt=datetime.datetime.now() - datetime.timedelta(minutes=20),
            raise_not_found_exception=False
        )
        if records:
            for record in records:
                status = record.status
                if not status == 'FAIL' or 'SUCCESS':
                    if status == 'WAIT_PROCESS':
                        self.update_item(
                            db=db,
                            find_by={'id': record.id},
                            update_to={'status': self.crud.STATUS_FAIL},
                        )
                        self.delete_item(
                            db=db,
                            find_by={'id': record.id}
                        )

                    if status in ['WAIT_WALLEX', 'WAIT_PAYMENT', 'PROCESS', 'WAIT_COLLATERAL']:
                        self.fund.cancel_fund_process(
                            db=db,
                            order_id=record.id,
                            user_id=record.user_id
                        )

                        self.update_item(
                            db=db,
                            find_by={'id': record.id},
                            update_to={'status': self.crud.STATUS_FAIL}
                        )

        db.commit()

    def get_order_details(self, page_number: int, page_size: int, **kwargs):
        data = {'result': [], 'total_count': None}
        result = self.crud.get_all_pay_orders(
            db=kwargs['db'],
            skip=(page_number - 1) * page_size,
            limit=page_size,
            **CqGetOrderDetails(**kwargs).dict()
        )
        query_result, total_count = result['query_result'], result['total_count']

        for item in query_result:
            order_obj = item[0]
            mobile_number = item[1]
            payment_id = item[2]
            data['result'].append(
                {
                    'id': order_obj.id,
                    'status': order_obj.status,
                    'title': order_obj.title,
                    'uuid': order_obj.identifier,
                    'user_id': order_obj.user_id,
                    'type': order_obj.type,
                    'amount': order_obj.amount,
                    'user_phone_number': mobile_number,
                    'merchant_user_id': order_obj.merchant_user_id,
                    'created_at': order_obj.created_at,
                    'paid_amount': item['paid_amount'],
                    'remain_amount': item['remain_amount'],
                    'commission': 0,
                    'first_payment_id': payment_id
                }
            )
        data['total_count'] = total_count
        return data

    def get_user_orders(self, page_number: int, page_size: int, **kwargs):
        data = {'result': [], 'total_count': None}
        result = self.crud.get_all_user_orders(
            db=kwargs['db'],
            skip=(page_number - 1) * page_size,
            limit=page_size,
            **CqGetUserOrders(**kwargs).dict()
        )
        query_result, total_count = result['query_result'], result['total_count']

        from user import UserService
        user_sr = UserService()
        user = user_sr.user.find_item_multi(
            db=kwargs['db'],
            id=kwargs['user_id']
        )[0]
        user_mobile_number = user.mobile

        for item in query_result:
            user_order_obj = item[0]
            credit_used_amount = item[1]
            gateway = item[2]
            data['result'].append(
                {
                    'id': user_order_obj.id,
                    'amount': user_order_obj.amount,
                    'merchant_user_id': user_order_obj.merchant_user_id,
                    'created_at': user_order_obj.created_at,
                    'commission': 0,
                    'user_phone_number': user_mobile_number,
                    'credit_used_amount': credit_used_amount,
                    'gateway': gateway,
                }
            )
        data['total_count'] = total_count
        return data

    # def check_action_validity(self, db: Session, uuid: str, action: str) -> pay_crud.model:
    #     if action in [self.crud.ACTION_REJECTED, self.crud.ACTION_APPROVED]:
    #         record = self.find_item_multi(db=db, identifier=uuid)[0]
    #
    #         diff = (datetime.datetime.now() - record.created_at).seconds / 60
    #         if int(diff) > settings.ORDER_REJECT_TIME:
    #             raise OrderActionTimeExpired
    #
    #         if record.action != self.crud.ACTION_UNVERIFIED:
    #             raise OrderActionIsNotUnverified
    #
    #         if record.status != self.crud.STATUS_SUCCESS:
    #             raise OrderStatusNotSuccess
    #
    #         return record
    #     else:
    #         raise OrderActionNotSupported
    #
    # def reject_action(self, db: Session, record: OrdPay) -> pay_crud.model:
    #     # Do some settle work for reject mode
    #     self.fund.delete_item()
    #     return record

    def get_all_merchant_orders(self, page_number: int, page_size: int, **kwargs):

        data = order_crud.get_orders(
            db=kwargs['db'],
            skip=(page_number - 1) * page_size,
            limit=page_size,
            **OrderGetSchema(**kwargs).dict()
        )

        return data

    @staticmethod
    def get_merchant_order(id: int, merchant_id: int = None, user_id: int = None, **kwargs):

        db = kwargs['db']

        order_data_queryset = db.query(
            OrdPay
        ).filter(
            OrdPay.deleted_at == None
        ).filter(
            OrdPay.id == id
        )

        if merchant_id:
            order_data_queryset = order_data_queryset.filter(
                OrdPay.merchant_id == merchant_id
            )

        if user_id:
            order_data_queryset = order_data_queryset.filter(
                OrdPay.user_id == user_id
            )

        order_data = order_data_queryset.first()

        result = None

        if order_data:

            result = OrderMerchantResponse(
                id=order_data.id,
                title=order_data.id,
                created_at=order_data.created_at,
                amount=order_data.amount,
                type=order_data.type,
                commission=OrderCommission(
                    id=order_data.commission.id,
                    category=order_data.commission.category,
                    pgw_commission_constant=order_data.commission.pgw_commission_constant,
                    pgw_commission_rate=order_data.commission.pgw_commission_rate,
                    pgw_fee_constant=order_data.commission.pgw_fee_constant,
                    pgw_fee_rate=order_data.commission.pgw_fee_rate,
                    credit_commission_constant=order_data.commission.credit_commission_constant,
                    credit_commission_rate=order_data.commission.credit_commission_rate,
                    credit_limit=order_data.commission.credit_limit,
                    decrease_fee_on_pay_gw_settle=order_data.commission.decrease_fee_on_pay_gw_settle,
                    decrease_commission_on_refund=order_data.commission.decrease_commission_on_refund
                ),
                status=order_data.status
            )

            credit_data_queryset = db.query(
                FncSettleCredit.amount
            ).filter(
                FncSettleCredit.deleted_at == None
            ).filter(
                FncSettleCredit.order_id == id
            )
            if merchant_id:
                credit_data_queryset = credit_data_queryset.filter(
                    FncSettleCredit.merchant_id == merchant_id
                )

            credit_data = credit_data_queryset.first()

            if credit_data:
                result.credit = credit_data.amount

            pgw_data_queryset = db.query(
                FncSettlePgw.amount
            ).filter(
                FncSettlePgw.deleted_at == None
            ).filter(
                FncSettlePgw.order_id == id
            )

            if merchant_id:
                pgw_data_queryset = pgw_data_queryset.filter(
                    FncSettlePgw.merchant_id == merchant_id
                )

            pgw_data = pgw_data_queryset.first()

            if pgw_data:
                result.pgw = pgw_data.amount

        return result


pay_agent = PayOrderInterface(
    crud=pay_crud,
    create_schema=CreatePayOrderSchema,
    update_schema=UpdatePayOrder,
    get_multi_schema=GetMultiOrdPay
)
