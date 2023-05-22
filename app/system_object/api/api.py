from enum import Enum

from fastapi import APIRouter

from .v1.endpoints import coins, rules, mobile


class Tags(Enum):
    coins = 'coins'
    rules = 'rules'
    mobile = 'mobile'


system_objects_router = APIRouter()

system_objects_router.include_router(
    rules.router,
    prefix="/v1/system-object/rules",
    tags=['system-objects'],
)

system_objects_router.include_router(
    coins.router,
    prefix="/v1/system-object/coins",
    tags=['system-objects'],
)

system_objects_router.include_router(
    mobile.router,
    prefix="/v1/system-object/mobile",
    tags=['system-objects'],
)
