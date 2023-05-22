from fastapi import APIRouter
from .v1.api import wallet_router, wallex_router, address_router, withdraw_router

user_assets_routes = [wallet_router, wallex_router, address_router, withdraw_router]

user_assets_router = APIRouter()

for route in user_assets_routes:
    user_assets_router.include_router(
        route,
        prefix="/v1/user-assets",
        tags=["user-assets"]
    )
