from sqlalchemy.orm import Session
from notification.notification_service import NotificationService
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.config import settings
from system.dbs.postgre import SessionLocal
from system_object import SystemObjectsService
from user import UserService
from .bank_profile import bank_profile_agent
from ..exceptions.refund import RefundAmountError, OrderStatusNotValidToRefund, OrderIsRefunding, OrderAlreadyRefunded
from ..models.refund import refund_crud, FncRefund
from ..models.schemas.refund import RefundGetMulti, RefundUpdate, RefundCreate


class RefundInterface(InterfaceBase):

    def __init__(
            self,
            crud: CRUDBase,
            create_schema,
            update_schema,
            get_multi_schema
    ):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = refund_crud
        self.model = FncRefund

    def _refund_user_side(
            self,
            refund_amount: int,
            debt_amount: int,
            user_id: int,
            order_id: int,
            refund_id: int,
            order_uuid: str,
            db: Session,
            iban_number: str = None,
            just_estimate: bool = False
    ):
        """
        if just_estimate is True it doesn't do anything and just estimating
        just_estimate=True --return_value--> refund_debt_amount, remain_refund_amount
        """
        from finance import FinanceService
        from order import OrderService
        from notification.notification_service import NotificationService

        order_sr = OrderService()
        finance_sr = FinanceService()
        user_sr = UserService()
        notification_sr = NotificationService()

        # get user to have user_first_name
        user_obj = user_sr.user.find_item_multi(
            db=db,
            id=user_id,
            return_first_obj=True
        )

        remain_refund_amount = refund_amount  # it will change
        total_debt_amount = debt_amount

        refund_debt_amount = 0  # use this just for estimation, it will increase
        transferred_money_amount = 0  # if transfer done successfully it will increase. It's in rial

        if remain_refund_amount < total_debt_amount and total_debt_amount:
            if not just_estimate:
                finance_sr.debt_user.decrease_debt(
                    order_id=order_id,
                    db=db,
                    user_id=user_id,
                    amount=abs(remain_refund_amount),
                    input_type='refund',
                    input_unique_id=refund_id
                )

                # repay
                order_sr.fund.repay_free_credit_from_refund(
                    order_id=order_id,
                    db=db,
                    user_id=user_id,
                    repay_amount=abs(remain_refund_amount)
                )

            refund_debt_amount += remain_refund_amount  # use this just for estimation
            total_debt_amount -= remain_refund_amount
            remain_refund_amount = 0

        if (remain_refund_amount >= total_debt_amount) and total_debt_amount:

            if not just_estimate:
                finance_sr.debt_user.decrease_debt(
                    order_id=order_id,
                    db=db,
                    user_id=user_id,
                    amount=abs(total_debt_amount),
                    input_type='refund',
                    input_unique_id=refund_id
                )

                # repay
                order_sr.fund.repay_free_credit_from_refund(
                    order_id=order_id,
                    db=db,
                    user_id=user_id,
                    repay_amount=abs(total_debt_amount)
                )
            refund_debt_amount += total_debt_amount  # use this just for estimation
            remain_refund_amount -= total_debt_amount

            total_debt_amount = 0

            # continue

        if not just_estimate and remain_refund_amount:
            bank_profile_obj = bank_profile_agent.find_item_multi(
                db=db,
                user_id=user_id,
                raise_not_found_exception=False,
                return_first_obj=True
            )

            transfer_dict = finance_sr.transfer.paya_transfer(
                bank_profile_id=bank_profile_obj.id,
                amount=abs(remain_refund_amount),
                description="money to refund order with id: " + str(order_id),
                input_type='refund',
                input_unique_id=refund_id
            )
            remain_refund_amount = 0
            transferred_money_amount += transfer_dict['amount']

        if just_estimate:
            return refund_debt_amount, remain_refund_amount
        else:
            # send sms to user and notify him that we refund his order
            notification_sr.notification_center.send_with_template(
                template_name='refunded_user_notified',
                template_key_values_dict={
                    "name": user_obj.first_name,
                    "order_uuid": order_uuid,
                    "tmn_amount": int(transferred_money_amount / 10),
                    'iban_number': iban_number,
                    'credit_amount': int(refund_debt_amount / 10),
                },
                user_id=user_id,
                with_sms=True,
                input_type="refund",
                input_unique_id=refund_id
            )

            self.update_item(
                db=db,
                find_by={'id': refund_id},
                update_to={'refund_by_debt': refund_debt_amount, "refund_by_rial": transferred_money_amount}
            )

    def _refund_merchant_side(
            self,
            db: Session,
            refund_amount: int,
            order_id: int,
            order_uuid: str,
            merchant_id: int,
            refund_id: int,
    ):
        from finance import FinanceService
        finance_sr = FinanceService()
        refund_obj = self.find_item_multi(db=db, id=refund_id, return_first_obj=True)
        refunded_by_debt = refund_obj.refund_by_debt
        refunded_by_rial = refund_obj.refund_by_rial

        remain_refund_amount = refund_amount
        settle_pgw_amount = 0
        settle_credit_amount = 0

        # # finding settle pgw of merchant for this order if exists
        # settle_pgw = finance_sr.settle_pgw.find_item_multi(
        #     db=db,
        #     order_id=order_id,
        #     type='pay',
        #     raise_not_found_exception=False,
        #     return_first_obj=True
        # )
        #
        # # finding settle credit of merchant for this order if exists
        # settle_credit = finance_sr.settle_credit.find_item_multi(
        #     db=db,
        #     order_id=order_id,
        #     type='pay',
        #     raise_not_found_exception=False,
        #     return_first_obj=True
        # )

        # if settle_pgw:
        #     settle_pgw_amount += settle_pgw.amount
        #
        # if settle_credit:
        #     settle_credit_amount += settle_credit.amount

        if refunded_by_debt:
            # the money that user paid by his debt I will transfer to user by settle credit in two weeks later
            finance_sr.settle_credit.decrease_amount(
                db=db,
                amount=refunded_by_debt,
                order_id=order_id,
                order_uuid=order_uuid,
                type='refund',
                merchant_id=merchant_id
            )

        if refunded_by_rial:
            # the money amount that I refunded to user directly the merchant should pay us directly
            finance_sr.settle_pgw.decrease_amount(
                db=db,
                amount=refunded_by_rial,
                order_id=order_id,
                order_uuid=order_uuid,
                type='refund',
                merchant_id=merchant_id
            )

        # while remain_refund_amount:
        #     if remain_refund_amount <= settle_credit_amount and settle_credit_amount:
        #         finance_sr.settle_credit.decrease_amount(
        #             db=db,
        #             amount=remain_refund_amount,
        #             order_id=order_id,
        #             order_uuid=order_uuid,
        #             type='refund',
        #             merchant_id=merchant_id
        #         )
        #         settle_credit_amount -= remain_refund_amount
        #         remain_refund_amount = 0
        #         continue
        #
        #     if remain_refund_amount > settle_credit_amount and settle_credit_amount:
        #         finance_sr.settle_credit.decrease_amount(
        #             db=db,
        #             amount=settle_credit_amount,
        #             order_id=order_id,
        #             order_uuid=order_uuid,
        #             type='refund',
        #             merchant_id=merchant_id
        #         )
        #         remain_refund_amount -= settle_credit_amount
        #         settle_credit_amount = 0
        #         continue
        #
        #     if remain_refund_amount <= settle_pgw_amount and settle_pgw_amount:
        #         finance_sr.settle_pgw.decrease_amount(
        #             db=db,
        #             amount=settle_credit_amount,
        #             order_id=order_id,
        #             order_uuid=order_uuid,
        #             type='refund',
        #             merchant_id=merchant_id
        #         )
        #         settle_pgw_amount -= remain_refund_amount
        #         remain_refund_amount = 0
        #         continue
        #
        #     if remain_refund_amount > settle_pgw_amount:
        #         raise SystemError("this line of algorithm should never touch")

    @staticmethod
    def _refund_validations(
            order_status: str,
            refund_amount: int,
            order_amount: int,

    ):
        from order import OrderService
        order_sr = OrderService()

        if order_status not in [
            order_sr.pay.crud.STATUS_REFUNDED,
            order_sr.pay.crud.STATUS_SUCCESS,
            order_sr.pay.crud.STATUS_WAIT_IBAN_TO_REFUND,
        ]:
            raise OrderStatusNotValidToRefund

        if order_status == order_sr.pay.crud.STATUS_REFUNDED:
            raise OrderAlreadyRefunded

        if refund_amount > order_amount:
            raise RefundAmountError

    def refund(
            self,
            order_uuid: str,
            merchant_id: int,
            merchant_user_id: int,
            refund_amount: int,
            db: Session
    ):
        try:
            from finance import FinanceService
            from order import OrderService

            order_sr = OrderService()
            user_sr = UserService()
            notification_sr = NotificationService()
            system_object_sr = SystemObjectsService()
            finance_sr = FinanceService()

            order = order_sr.pay.find_item_multi(
                db=db,
                identifier=order_uuid,
                return_first_obj=True,
                merchant_id=merchant_id
            )

            # respect to idempotency
            if order.status == order_sr.pay.crud.STATUS_REFUNDED:
                return {
                    'order_status': 'ALREADY_REFUNDED',
                    'order_uuid': order_uuid
                }

            # Raise error if any validation problem
            self._refund_validations(order_status=order.status, refund_amount=refund_amount, order_amount=order.amount)

            merchant = user_sr.merchant.find_item_multi(
                db=db,
                id=merchant_id,
                return_first_obj=True
            )

            order_user = user_sr.user.find_item_multi(db=db, id=order.user_id, return_first_obj=True)

            bank_profile_obj = bank_profile_agent.find_item_multi(
                db=db,
                user_id=order_user.id,
                raise_not_found_exception=False,
                return_first_obj=True
            )

            refund_obj = self.find_item_multi(
                db=db,
                order_id=order.id,
                return_first_obj=True,
                raise_not_found_exception=False
            )

            if not refund_obj:
                # add refund record with 'REQUESTED_FROM_MERCHANT'
                tmp_session = SessionLocal()
                refund_obj = self.add_item(
                    db=tmp_session,
                    order_uuid=order_uuid,
                    order_id=order.id,
                    merchant_id=merchant_id,
                    merchant_user_id=merchant_user_id,
                    amount=refund_amount,
                    order_user_id=order.user_id,
                    status='REQUESTED_FROM_MERCHANT'
                )
                tmp_session.commit()
                tmp_session.close()

            # get it twice
            refund_obj = self.find_item_multi(
                db=db,
                order_id=order.id,
                return_first_obj=True,
                raise_not_found_exception=False
            )

            # Refund user side
            refund_debt_amount, refund_rial_amount = self._refund_user_side(
                db=db,
                refund_amount=refund_amount,
                debt_amount=finance_sr.debt_user.get_total_debt_of_order(
                    db=db,
                    order_id=order.id,
                    user_id=order.user_id
                ),
                user_id=order_user.id,
                order_id=order.id,
                refund_id=refund_obj.id,
                order_uuid=order_uuid,
                iban_number=bank_profile_obj.iban if bank_profile_obj else None,
                just_estimate=True
            )

            # bank_profile info should be complete
            if refund_rial_amount and (not bank_profile_obj or not bank_profile_obj.iban):
                # if not order_user.first_name or not order_user.last_name:
                #     raise SystemError("user should have first_name and last_name")

                # send sms to user to update the iban number
                notification_sr.notification_center.send_with_template(
                    template_name='get_card_number_to_refund',
                    template_key_values_dict={
                        'name': str(order_user.first_name) + " " + str(order_user.last_name),
                        'merchant_name': merchant.name,
                        'link': settings.UPDATE_USER_BANK_NUMBER_PROFILE_FOR_REFUND_URL
                    },
                    user_id=order.user_id,
                    with_sms=True
                )

                # update order status to wait for iban to refund
                order_sr.pay.update_item(
                    db=db,
                    find_by={'id': order.id},
                    update_to={'status': order_sr.pay.crud.STATUS_WAIT_IBAN_TO_REFUND}
                )

                return {
                    'order_status': order_sr.pay.crud.STATUS_WAIT_IBAN_TO_REFUND,
                    'order_uuid': order_uuid
                }

            # Refund user side
            self._refund_user_side(
                db=db,
                refund_amount=refund_amount,
                debt_amount=finance_sr.debt_user.get_total_debt_of_order(
                    db=db,
                    order_id=order.id,
                    user_id=order.user_id
                ),
                user_id=order_user.id,
                order_id=order.id,
                refund_id=refund_obj.id,
                order_uuid=order_uuid,
                iban_number=bank_profile_obj.iban if bank_profile_obj else None,
            )

            # Refund merchant side
            self._refund_merchant_side(
                db=db,
                refund_amount=refund_amount,
                order_id=order.id,
                order_uuid=order_uuid,
                merchant_id=merchant_id,
                refund_id=refund_obj.id
            )

            # update order status to refunded
            order_sr.pay.update_item(
                db=db, find_by={'identifier': order_uuid}, update_to={'status': order_sr.pay.crud.STATUS_REFUNDED}
            )

            # update refund record status to 'DONE'
            refund_agent.update_item(
                db=db, find_by={'order_id': order.id}, update_to={'status': 'DONE'}
            )

            return {
                'order_status': order_sr.pay.crud.STATUS_REFUNDED,
                'order_uuid': order_uuid
            }
        except Exception as e:
            raise e

    def get_refund_detail(
            self,
            db: Session,
            order_uuid: str,
            user_id: int,
    ):
        try:
            from finance import FinanceService
            from order import OrderService
            from user import UserService

            finance_sr = FinanceService()
            order_sr = OrderService()
            user_sr = UserService()

            # Local Vars
            refund_debt_amount = 0
            refund_rial_amount = 0


            # get order obj and also validate that the user should be owner of order
            order_obj = order_sr.pay.find_item_multi(
                db=db,
                identifier=order_uuid,
                user_id=user_id,
                return_first_obj=True,
            )

            # get merchant obj
            merchant_obj = user_sr.merchant.find_item_multi(
                db=db,
                id=order_obj.merchant_id,
                return_first_obj=True
            )

            # get refund obj
            refund_obj = self.find_item_multi(db=db, order_id=order_obj.id, return_first_obj=True)

            if order_obj.status in [order_sr.pay.crud.STATUS_REFUNDING, order_sr.pay.crud.STATUS_WAIT_IBAN_TO_REFUND]:
                refund_debt_amount, refund_rial_amount = self._refund_user_side(
                    db=db,
                    refund_amount=refund_obj.amount,
                    debt_amount=finance_sr.debt_user.get_total_debt_of_order(
                        db=db,
                        order_id=order_obj.id,
                        user_id=user_id
                    ),
                    user_id=user_id,
                    order_id=order_obj.id,
                    refund_id=0,
                    just_estimate=True,
                    order_uuid=order_uuid
                )
            else:
                refund_debt_amount += refund_obj.refund_by_debt
                refund_rial_amount += refund_obj.refund_by_rial

            return {
                'merchant_logo_address': merchant_obj.logo_address,
                'merchant_name_fa': merchant_obj.name_fa,
                'order_total_amount': order_obj.amount,
                'credit_amount_to_refund': refund_debt_amount,
                'tmn_amount_to_refund': refund_rial_amount  # it will convert to rial in schema, in facts its rial
            }
        except Exception as e:
            # db.rollback()
            raise e

    def submit_refund_after_user_create_bank_profile(
            self,
            order_uuid: str,
            user_id: int,
            db: Session
    ):
        from order import OrderService
        order_sr = OrderService()

        # get order and validate that this order is valid to refund and also refund from this user
        order_obj = order_sr.pay.find_item_multi(
            db=db,
            identifier=order_uuid,
            user_id=user_id,
            status=order_sr.pay.crud.STATUS_WAIT_IBAN_TO_REFUND,
            return_first_obj=True
        )

        # get refund obj
        refund_obj = self.find_item_multi(
            db=db,
            order_id=order_obj.id,
            return_first_obj=True
        )

        return self.refund(
            db=db,
            order_uuid=order_uuid,
            merchant_id=order_obj.merchant_id,
            merchant_user_id=user_id,
            refund_amount=refund_obj.amount
        )


refund_agent = RefundInterface(
    crud=refund_crud,
    create_schema=RefundCreate,
    update_schema=RefundUpdate,
    get_multi_schema=RefundGetMulti
)
