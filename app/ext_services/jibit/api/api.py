from fastapi import APIRouter
from ext_services.jibit.api.api_v1.endpoints import jibit_pay_gateway_callback
from ext_services.jibit.api.api_v1.endpoints import inquiry

jibit_router = APIRouter()

jibit_router.include_router(
    jibit_pay_gateway_callback.router,
    prefix="/v1/jibit/payment_gateway_callback",
    tags=["jibit"],
    responses={404: {"description": "Not found"}}
)

jibit_router.include_router(
    inquiry.router,
    prefix="/v1/jibit/payment_gateway_inquiry",
    tags=["jibit"],
    responses={404: {"description": "Not found"}}
)




