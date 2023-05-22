from fastapi import APIRouter

from .endpoints import wallex, wallet

address_router = APIRouter()
# user_asset_router = APIRouter()
wallex_router = APIRouter()
wallet_router = APIRouter()
withdraw_router = APIRouter()

wallet_router.include_router(
    wallet.router,
    prefix='/wallet'
)

wallex_router.include_router(
    wallex.router,
    prefix='/wallex'
)
