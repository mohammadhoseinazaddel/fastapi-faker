from fastapi import APIRouter
from ..v1.endpoints import (

    bank_pay,
    bank_profile,
    payment_gateway,
    refund,
    finance_admin,
    finance_merchant,
)

finance_router = APIRouter()
finance_merchant_router = APIRouter()
finance_admin_router = APIRouter()

finance_router.include_router(
    bank_pay.router,
    prefix='/bank/payment',
    tags=['finance']
)

finance_router.include_router(
    bank_profile.router,
    prefix='/bank-profile',
    tags=['finance']
)

finance_router.include_router(
    payment_gateway.router,
    prefix='/payment-gateway',
    tags=['finance']
)

finance_router.include_router(
    refund.router,
    prefix='/refund',
    tags=['finance']
)

finance_merchant_router.include_router(
    finance_merchant.router,
    prefix='/merchant',
    tags=['finance-merchant']
)

finance_admin_router.include_router(
    finance_admin.router,
    prefix='/admin',
    tags=['finance-admin']
)
