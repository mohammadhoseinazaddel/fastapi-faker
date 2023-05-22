from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from system.scopes.order import order_scopes

from user.interfaces.user import UserInterface
from utils import redirect_no_cache, ResponseManager
from .order_merchant import order_merchant_all, order_merchant
from ..schemas.pay import *

router = APIRouter()

pay_info_RM = ResponseManager(
    request_model=None,
    response_model=PayInfoResponse,
    pagination=False,
    is_mock=False
)


@router.get(
    "/info", response_model=pay_info_RM.response_model(), response_description="Get Order Info"
)
async def get_order_info(order_uuid: str, db: Session = Depends(get_db)):
    try:
        from user import UserService
        from order import OrderService

        user_sr = UserService()
        order_sr = OrderService()

        order = order_sr.pay.find_item_multi(db=db, identifier=order_uuid)[0]
        if order:
            merchant = user_sr.merchant.find_item_multi(db=db, id=order.merchant_id)[0]

            pay_info_RM.status_code(200)
            return pay_info_RM.response(
                {
                    "uuid": order.identifier,
                    "merchant_name_fa": merchant.name_fa,
                    "amount": order.amount,
                    "merchant_logo": merchant.logo_address,
                    "status": order.status,
                }
            )
    except Exception as e:
        return pay_info_RM.exception(e)


pay_create_RM = ResponseManager(
    request_model=PayCreateRequest,
    response_model=PayCreateResponse,
    pagination=False,
    is_mock=False
)


@router.post(
    "/create",
    response_model=pay_create_RM.response_model(),
    response_description="Register Order from Merchant",
)
def create_order(
        request_model: pay_create_RM.request_model(),
        # current_user_id: str = Security(UserInterface.get_current_user, scopes=["order:pay:create"]),
        db: Session = Depends(get_db),
):
    """
    Merchant will call this api to create an order without user id
    after that in 'submit-order' api we will set the user_id of that order
    """
    try:
        from order.order_service import OrderService
        from finance import FinanceService

        order_sr = OrderService()

        commission = order_sr.commission.find_item_multi(
            db=db,
            category=request_model.commission,
            merchant_id=request_model.merchant_id
        )[0]

        created_order = order_sr.pay.add_item(
            db=db,
            merchant_order_id=request_model.order_id,
            merchant_id=request_model.merchant_id,
            merchant_user_id=request_model.user_id,
            type=request_model.type,
            amount=request_model.amount,
            merchant_redirect_url=request_model.callback_url,
            title=request_model.title,
            commission_id=commission.id,
        )

        pay_create_RM.status_code(201)
        return pay_create_RM.response(
            {
                "uuid": created_order.identifier,
                "callback_url": settings.FRONT_BASE_URL + f"/payment/order?id={created_order.identifier}",
            }
        )

    except Exception as e:
        db.rollback()
        return pay_create_RM.exception(e)


pay_process_RM = ResponseManager(
    request_model=PayProcessRequest,
    response_model=PayProcessResponse,
    pagination=False,
    is_mock=False
)


@router.post(
    "/process",
    response_model=pay_process_RM.response_model(),
    response_description="Process User Order",
)
async def process_order(
        request_model: pay_process_RM.request_model() = Depends(pay_process_RM.request_model()),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["order:pay:process"]),
        db: Session = Depends(get_db),
):
    try:
        from finance import FinanceService
        from user import UserService
        from order import OrderService
        from system_object import SystemObjectsService
        from credit import CreditService

        order_sr = OrderService()
        sys_obj_sr = SystemObjectsService()
        user_sr = UserService()
        credit_sr = CreditService()

        # Find Pay order
        pay_order = order_sr.pay.check_order_validity(db=db, uuid=request_model.uuid)
        order_status = pay_order.status

        if order_status == order_sr.pay.crud.STATUS_WAIT_PROCESS:

            # register order to user
            await order_sr.pay.register_order_to_user(db=db, user_id=current_user_id, uuid=request_model.uuid)

            # calculate credit
            calculate_credit_obj = credit_sr.calculator.calculate_credit(
                db=db,
                user_id=current_user_id,
                input_type="pay-order",
                input_unique_id=pay_order.id,
            )

            free_credit = calculate_credit_obj.free_credit - calculate_credit_obj.used_free_credit
            if free_credit < 0:
                free_credit = 0
            # non_free_credit = calculate_credit_obj.non_free_credit - calculate_credit_obj.used_non_free_credit

            # Create fund
            fund = order_sr.fund.make_fund(
                order_id=pay_order.id,
                order_identifier=pay_order.identifier,
                order_amount=pay_order.amount,
                order_type=pay_order.type,
                free_credit=free_credit,
                cs=calculate_credit_obj.cs,
                user_id=current_user_id,
                db=db,
            )
            if fund['need_collateral']:
                order_sr.pay.update_item(
                    db=db,
                    find_by={'id': pay_order.id},
                    update_to={
                        'user_id': current_user_id,
                        'status': order_sr.pay.crud.STATUS_WAIT_COLLATERAL
                    }
                )
            elif fund['need_payment']:
                order_sr.pay.update_item(
                    db=db,
                    find_by={"id": pay_order.id},
                    update_to={"user_id": current_user_id, "status": order_sr.pay.crud.STATUS_WAIT_PAYMENT},
                )
            else:
                order_sr.pay.update_item(
                    db=db,
                    find_by={"id": pay_order.id},
                    update_to={
                        "user_id": current_user_id,
                        "status": order_sr.pay.crud.STATUS_PROCESS,
                    },
                )
        else:
            order_sr.pay.check_order_user_validity(record=pay_order, user_id=current_user_id)

        calculate_credit_obj = credit_sr.calculator.find_item_multi(
            db=db, input_type="pay-order", input_unique_id=pay_order.id
        )[0]
        merchant = user_sr.merchant.find_item_multi(db=db, id=pay_order.merchant_id)[0]
        # merchant = 1
        fund = order_sr.fund.find_item_multi(db=db, order_id=pay_order.id)[0]

        use_collateral = False
        if fund.used_non_free_credit or fund.need_wallex_asset:
            use_collateral = True

        user_credit = credit_sr.calculator.get_total_credit(
            db=db, calculate_id=calculate_credit_obj.id
        )

        used_non_free_credit = 0
        if fund.need_collateral:
            collateral_list = order_sr.fund.get_collateral(db=db, fund=fund)
            for collateral in collateral_list:
                used_non_free_credit += collateral['blocked_amount_in_tmn']

        pay_process_RM.status_code(200)
        return pay_process_RM.response(
            {
                "uuid": pay_order.identifier,
                "type": pay_order.type,
                "status": pay_order.status,
                "merchant_name_fa": merchant.name_fa,
                "merchant_logo": merchant.logo_address,
                "user_credit": user_credit,
                "in_use_credit": fund.used_free_credit + used_non_free_credit,
                "amount": pay_order.amount,
                "use_collateral": use_collateral,
                "order_price": pay_order.amount,
                "amount_to_pay": fund.payment_amount,
            }
        )

    except Exception as e:
        db.rollback()
        return pay_process_RM.exception(e)


pay_result_RM = ResponseManager(
    request_model=None,
    response_model=PayResultResponse,
    pagination=False,
    is_mock=False
)


@router.get("/result/{uuid}", response_description="result of order process",
            response_model=pay_result_RM.response_model())
def pay_order_result(
        uuid: str, db: Session = Depends(get_db),
):
    try:
        from ext_services.wallex.interfaces.pay import wallex_pay_agent
        from finance import FinanceService
        from user_assets import UserAssetsService
        from order import OrderService

        order_sr = OrderService()
        finance_sr = FinanceService()
        user_assets_sr = UserAssetsService()

        # # Find Pay order
        order = order_sr.pay.check_order_validity(db=db, uuid=uuid)

        if order.status == "WAIT_COLLATERAL":
            return pay_result_RM.response(
                {"redirect_url": settings.FRONT_COLLATERAL_CONFIRM_URL + order.identifier}
            )
            # return redirect_no_cache(url=settings.FRONT_COLLATERAL_CONFIRM_URL + order.identifier)

        if order.status == "WAIT_WALLEX":
            fund = order_sr.fund.find_item_multi(db=db, order_id=order.id)[0]
            wallex_pay = wallex_pay_agent.find_item_multi(
                db=db, token=fund.wallex_block_request_id
            )[0]
            url = wallex_pay.redirect_url
            return pay_result_RM.response(
                {"redirect_url": url}
            )
            # return RedirectResponse(url, status_code=307)

        if order.status == "WAIT_PAYMENT":
            fund = order_sr.fund.find_item_multi(db=db, order_id=order.id)[0]
            bank_url = finance_sr.bank.gateway.get_switching_url(
                bank_payment_id=fund.payment_id,
                db=db,
            )["psp_switching_url"]
            return pay_result_RM.response(
                {"redirect_url": bank_url}
            )

        if order.status == "PROCESS":
            fund = order_sr.fund.find_item_multi(db=db, order_id=order.id)[0]
            if fund.need_wallex_asset:
                result = user_assets_sr.wallex_transaction.find_blocked_coins(
                    db=db, input_type='fund', input_unique_id=fund.id
                )
                for coin_name, balance in result.items():
                    if balance:
                        user_assets_sr.wallex_transaction.freeze_balance(
                            user_id=order.user_id,
                            coin_name=coin_name,
                            input_type="fund",
                            input_unique_id=fund.id,
                            amount=balance,
                            db=db,
                        )
                wallex_pay_agent.api_confirm_request(token=fund.wallex_block_request_id)

            if fund.used_asset_json and fund.used_asset_json["wallpay"]:
                result = user_assets_sr.crypto_transaction.find_blocked_coins(
                    db=db, input_type="fund", input_unique_id=fund.id
                )
                for coin_name, balance in result.items():
                    if balance:
                        user_assets_sr.crypto_transaction.freeze_balance(
                            user_id=order.user_id,
                            coin_name=coin_name,
                            input_type="fund",
                            input_unique_id=fund.id,
                            amount=balance,
                            db=db,
                        )

            # change order status
            order_sr.pay.update_item(
                db=db,
                find_by={"id": order.id},
                update_to={"status": order_sr.pay.crud.STATUS_SUCCESS},
            )

            # success finance settle
            finance_sr.settle.order_manager(
                db=db,
                merchant_id=order.merchant_id,
                user_id=order.user_id,
                order_id=order.id,
                order_uuid=order.identifier,
                order_status=order.status,
                used_credit=fund.used_free_credit,
                extra_payment_amount=fund.extra_money_to_pay,
                commission_id=order.commission_id
            )

            url = (
                    order.merchant_redirect_url
                    + f"?status={order.status}"
                      f"&uuid={order.identifier}"
                      f"&order_id={order.merchant_order_id}"
                      f"&user_id={order.merchant_user_id}"
            )
            return pay_result_RM.response(
                {"redirect_url": url}
            )

        if order.status in ['SUCCESS', 'FAIL']:
            url = (
                    order.merchant_redirect_url
                    + f"?status={order.status}"
                      f"&uuid={order.identifier}"
                      f"&order_id={order.merchant_order_id}"
                      f"&user_id={order.merchant_user_id}"
            )

            return pay_result_RM.response(
                {"redirect_url": url}
            )

        if order.status in ["FAIL_FILL", "FAIL_WALLEX", "FAIL_PAYMENT"]:
            order_sr.fund.cancel_fund_process(db=db, order_id=order.id, user_id=order.user_id)

            # change status to fail
            order_sr.pay.update_item(
                db=db, find_by={"id": order.id}, update_to={"status": order_sr.pay.crud.STATUS_FAIL}
            )

            # success finance settle
            fund = order_sr.fund.find_item_multi(
                db=db,
                order_id=order.id
            )[0]
            finance_sr.settle.order_manager(
                db=db,
                merchant_id=order.merchant_id,
                user_id=order.user_id,
                order_id=order.id,
                order_uuid=order.identifier,
                order_status=order.status,
                used_credit=fund.used_free_credit,
                extra_payment_amount=fund.extra_money_to_pay,
                commission_id=order.commission_id
            )

            # return redirect_no_cache(url=settings.FRONT_FAIL_LANDING_URL + order.identifier)
            return pay_result_RM.response(
                {"redirect_url": settings.FRONT_SUCCESS_LANDING_URL + order.identifier}
            )

    except Exception as e:
        db.rollback()
        return pay_process_RM.exception(e)


@router.get("/callback/{uuid}")
def pay_order_callback(uuid: str, db: Session = Depends(get_db)):
    try:
        from finance import FinanceService
        from order import OrderService
        from ext_services.wallex.interfaces.pay import wallex_pay_agent

        finance_sr = FinanceService()
        order_sr = OrderService()

        order = order_sr.pay.find_item_multi(db=db, identifier=uuid)[0]
        fund = order_sr.fund.find_item_multi(db=db, order_id=order.id)[0]

        if "WAIT" in order.status:

            if order.status == order_sr.pay.crud.STATUS_WAIT_COLLATERAL:
                order_sr.fund.block_wallpay_asset_by_json(
                    db=db,
                    fund=fund
                )
                if fund.need_wallex_asset:
                    order_sr.fund.create_wallex_block_request(db=db, fund=fund, order_uuid=order.identifier)
                    # update order status
                    order_sr.pay.update_item(
                        db=db,
                        find_by={"id": order.id},
                        update_to={"status": order_sr.pay.crud.STATUS_WAIT_WALLEX},
                    )
                else:
                    # update fund
                    fund.collateral_confirmed = True
                    order_sr.fund.get_payment_id(
                        db=db,
                        order_identifier=order.identifier,
                        fund=fund
                    )

            if order.status == order_sr.pay.crud.STATUS_WAIT_WALLEX:
                wallex_pay_record = wallex_pay_agent.find_item_multi(db=db, token=fund.wallex_block_request_id)[0]
                wallex_pay_status = wallex_pay_record.status

                if wallex_pay_status == 'UNVERIFIED':
                    order_sr.fund.block_wallex_asset_by_json(
                        db=db,
                        fund=fund
                    )
                    # update fund
                    fund.collateral_confirmed = True
                    order_sr.fund.get_payment_id(
                        db=db,
                        order_identifier=order.identifier,
                        fund=fund
                    )

                if wallex_pay_status in ['REJECTED_BY_USER', 'REJECTED_BY_SYSTEM']:
                    order_sr.pay.update_item(
                        db=db,
                        find_by={"id": order.id},
                        update_to={"status": order_sr.pay.crud.STATUS_FAIL_WALLEX},
                    )

            if fund.collateral_confirmed:
                if fund.payment_id:
                    # update order status
                    order_sr.pay.update_item(
                        db=db,
                        find_by={"id": order.id},
                        update_to={"status": order_sr.pay.crud.STATUS_WAIT_PAYMENT},
                    )
                else:
                    # update order status
                    order_sr.pay.update_item(
                        db=db,
                        find_by={"id": order.id},
                        update_to={"status": order_sr.pay.crud.STATUS_PROCESS},
                    )

            if order.status == order_sr.pay.crud.STATUS_WAIT_PAYMENT:
                bank_payment_db_obj = finance_sr.bank.payment.find_item_multi(db=db, id=fund.payment_id)[0]
                bank_payment_status = bank_payment_db_obj.status

                if bank_payment_status == "PAID":
                    # update fund paid at
                    order_sr.fund.update_item(
                        db=db, find_by={"id": fund.id}, update_to={"paid_at": datetime.now()}
                    )

                    # update order status
                    order_sr.pay.update_item(
                        db=db,
                        find_by={"id": order.id},
                        update_to={"status": order_sr.pay.crud.STATUS_PROCESS},
                    )
                if bank_payment_status == "FAILED":
                    # update order status
                    order_sr.pay.update_item(
                        db=db,
                        find_by={"id": order.id},
                        update_to={"status": order_sr.pay.crud.STATUS_FAIL_PAYMENT},
                    )

        url = f"/api/v1/order/pay/result/{order.identifier}"
        return redirect_no_cache(url=url)

    except Exception as e:
        db.rollback()
        return pay_process_RM.exception(e)


pay_action_RM = ResponseManager(
    request_model=None,
    response_model=PayActionResponse,
    pagination=False,
    is_mock=False
)


@router.get(
    "/{action}/{uuid}",
    response_model=pay_action_RM.response_model(),
    response_description="result of order process")
def pay_order_action(
        uuid: str,
        action: str,
        db: Session = Depends(get_db),
):
    try:
        from order import OrderService
        order_sr = OrderService()

        # Find Pay order
        order = order_sr.pay.check_order_validity(db=db, uuid=uuid)

        pay_info_RM.status_code(200)
        return pay_action_RM.response(
            order_sr.pay.update_order_action(
                db=db,
                record=order,
                action=action
            )
        )

    except Exception as e:
        db.rollback()
        return pay_action_RM.exception(e)


pay_my_orders_RM = ResponseManager(
    request_model=None,
    response_model=PayMyOrdersResponse,
    pagination=True,
    is_mock=True,
    is_list=True
)


@router.get(
    '/my-orders',
    response_description="user Orders List",
    response_model=order_merchant_all.response_model()
)
def pay_order_user_items(
        request: order_merchant_all.request_model() = Depends(order_merchant_all.request_model()),
        current_user_id: int = Security(UserInterface.get_current_user,
                                        scopes=[order_scopes["order:pay:my-orders"]["name"]]),
        db: Session = Depends(get_db),
):
    try:
        from order import OrderService
        order_sr = OrderService()
        data = order_sr.pay.get_all_merchant_orders(
            db=db,
            page_number=request.page_number,
            page_size=request.page_size,
            created_at_gte=request.start_time,
            created_at_lte=request.end_time,
            type=request.type,
            commission=request.commission_id,
            status=request.status,
            user_id=current_user_id
        )

        order_merchant_all.pagination_data(
            total_count=data["total_count"],
            current_page=request.page_number,
            page_size=request.page_size
        )
        order_merchant_all.status_code(200)

        return order_merchant_all.response(data["query_result"])

    except Exception as e:
        return order_merchant_all.exception(e)


@router.get(
    '/{id}',
    response_description="user order details",
    response_model=order_merchant.response_model()
)
async def user_order(
        id: int,
        current_user_id: int = Security(UserInterface.get_current_user, scopes=[order_scopes["order:pay:my-orders"]["name"]]),
        db: Session = Depends(get_db),
):
    try:
        from order import OrderService
        order_sr = OrderService()

        result = order_sr.pay.get_merchant_order(db=db, id=id, user_id=current_user_id)

        if result:
            order_merchant.status_code(200)
            return order_merchant.response(result.dict())
        order_merchant.status_code(404)
        return order_merchant.response(None)

    except Exception as e:
        return order_merchant.exception(e)

