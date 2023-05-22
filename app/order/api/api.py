from fastapi import APIRouter

from .v1.api import order_router, order_admin_router, order_merchant_router

order_routes = [order_router, order_admin_router, order_merchant_router]

order_router = APIRouter()

for route in order_routes:
    order_router.include_router(
        route,
        prefix="/v1/order",
    )
