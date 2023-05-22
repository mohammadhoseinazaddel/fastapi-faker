import datetime
from typing import Literal

from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session

from system.dbs.postgre import get_db
from utils import ResponseManager
from user.interfaces.user import UserInterface
from ..schemas.order_admin import *

router = APIRouter()

pay_RM = ResponseManager(
    request_model=None,
    response_model=PayOrderDetailResponse,
    pagination=True,
    is_mock=True,
    is_list=True
)


@router.get(
    '/all',
    response_description="order detail",
    response_model=pay_RM.response_model()
)
async def all_orders(
        order_status: Literal['SUCCESS', 'FAIL', 'WAIT'],
        phone_number: str = None,
        created_at_ge: datetime.datetime = None,
        created_at_le: datetime.datetime = None,
        order_price_ge: float = None,
        order_price_le: float = None,
        page_number: int = Query(default=1, ge=1),
        admin_user_id: str = Security(UserInterface.get_current_user, scopes=["order:pay:all-orders"]),
        db: Session = Depends(get_db),

):
    from order import OrderService
    order_sr = OrderService()

    try:
        result = order_sr.pay.get_order_details(
            db=db,
            phone_number=phone_number,
            created_at_ge=created_at_ge,
            created_at_le=created_at_le,
            order_price_le=order_price_le * 10 if order_price_le else None,
            order_price_ge=order_price_ge * 10 if order_price_ge else None,
            order_status=order_status,
            page_number=page_number,
            page_size=10
        )

        pay_RM.pagination_data(total_count=result['total_count'], current_page=page_number, page_size=10)
        pay_RM.status_code(200)
        return pay_RM.response(result['result'])
    except Exception as e:
        return pay_RM.exception(e)


user_order_RM = ResponseManager(
    request_model=None,
    response_model=UserOrdersResponse,
    pagination=True,
    is_mock=False,
    is_list=True
)


@router.get(
    '/user-orders',
    response_description="user orders",
    response_model=user_order_RM.response_model()
)
async def all_user_orders(
        created_at_ge: datetime.datetime = None,
        created_at_le: datetime.datetime = None,
        page_number: int = Query(default=1, ge=1),
        order_price_ge: float = None,
        order_price_le: float = None,
        current_user_id: str = Security(UserInterface.get_current_user, scopes=["order:pay:user-orders"]),
        user_id: int = Query(),
        db: Session = Depends(get_db),

):
    from order import OrderService
    order_sr = OrderService()

    try:

        result = order_sr.pay.get_user_orders(
            db=db,
            user_id=user_id,
            created_at_ge=created_at_ge,
            created_at_le=created_at_le,
            order_price_le=order_price_le * 10 if order_price_le else None,
            order_price_ge=order_price_ge * 10 if order_price_ge else None,
            page_number=page_number,
            page_size=10
        )

        user_order_RM.pagination_data(total_count=result['total_count'], current_page=page_number, page_size=10)
        user_order_RM.status_code(200)
        return user_order_RM.response(result['result'])
    except Exception as e:
        return user_order_RM.exception(e)
