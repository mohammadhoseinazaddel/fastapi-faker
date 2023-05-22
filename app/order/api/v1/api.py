from fastapi import APIRouter

from .endpoints import pay, order_admin, order_merchant

order_router = APIRouter()
order_admin_router = APIRouter()
order_merchant_router = APIRouter()

order_router.include_router(
    pay.router,
    prefix="/pay",
    tags=["order"]
)

order_admin_router.include_router(
    order_admin.router,
    prefix='/admin',
    tags=["order-admin"]
)

order_merchant_router.include_router(
    order_merchant.router,
    prefix='/merchant',
    tags=["order-merchant"]
)
