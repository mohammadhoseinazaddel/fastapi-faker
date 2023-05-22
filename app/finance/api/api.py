from fastapi import APIRouter
from .v1.api import finance_router, finance_merchant_router, finance_admin_router

finance_routes = [finance_router, finance_merchant_router, finance_admin_router]

finance_router = APIRouter()

for route in finance_routes:
    finance_router.include_router(
        route,
        prefix="/v1/finance",
    )
