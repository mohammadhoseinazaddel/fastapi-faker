from fastapi import APIRouter

from .endpoints import otp, login, merchants, user_admin, user

user_router = APIRouter()
user_admin_router = APIRouter()
otp_router = APIRouter()
login_router = APIRouter()
merchant_router = APIRouter()

user_router.include_router(
    user.router,
    tags=['user']
)

user_router.include_router(
    user_admin.router,
    tags=['user-admin']
)

otp_router.include_router(
    otp.router,
    prefix='/otp',
    tags=['user']

)

login_router.include_router(
    login.router,
    prefix='/login',
    tags=['user']
)

merchant_router.include_router(
    merchants.router,
    prefix='/merchant',
    tags=['user-merchant']
)
