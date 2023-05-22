from fastapi import APIRouter
from .v1.api import user_router, otp_router, login_router, merchant_router

user_routes = [user_router, otp_router, login_router, merchant_router]

user_router = APIRouter()

for route in user_routes:
    user_router.include_router(
        route,
        prefix="/v1/user",
    )
