from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from utils import ResponseManager
from system.scopes.order import order_scopes
from user.interfaces.user import UserInterface
from ..schemas.order_merchant import *

router = APIRouter()

order_merchant_all = ResponseManager(
    request_model=OrdersMerchantRequest,
    response_model=OrdersMerchantResponse,
    pagination=True,
    is_mock=False,
    is_list=True
)


@router.get(
    '/all',
    response_description="Merchant Orders List",
    response_model=order_merchant_all.response_model()
)
async def merchant_orders(
        request: order_merchant_all.request_model() = Depends(order_merchant_all.request_model()),
        current_user_id: str = Security(UserInterface.get_current_user, scopes=[order_scopes["merchant:all"]["name"]]),
        db: Session = Depends(get_db),
):
    user = UserInterface.find_by_id(user_id=current_user_id, db=db)

    try:
        from order import OrderService
        order_sr = OrderService()

        data = order_sr.pay.get_all_merchant_orders(
            db=db,
            page_number=request.page_number,
            page_size=request.page_size,
            created_at_gte=request.start_time,
            created_at_lte=request.end_time,
            order_id=request.order_id,
            type=request.type,
            commission_id=request.commission_id,
            status=request.status,
            merchant_id=user.merchant.id
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


order_merchant = ResponseManager(
    request_model=None,
    response_model=OrderMerchantResponse,
    pagination=False,
    is_mock=False,
    is_list=True
)


@router.get(
    '/{id}',
    response_description="Merchant Order",
    response_model=order_merchant.response_model()
)
async def merchant_order(
        id: int,
        current_user_id: str = Security(UserInterface.get_current_user, scopes=[order_scopes["merchant:all"]["name"]]),
        db: Session = Depends(get_db),
):
    user = UserInterface.find_by_id(user_id=current_user_id, db=db)

    try:
        from order import OrderService
        order_sr = OrderService()

        result = order_sr.pay.get_merchant_order(db=db, id=id, merchant_id=user.merchant.id)

        if result:
            order_merchant.status_code(200)
            return order_merchant.response(result.dict())
        order_merchant.status_code(404)
        return order_merchant.response(None)

    except Exception as e:
        return order_merchant.exception(e)
