from fastapi import APIRouter
from .v1.api import credit_router, credit_admin_router

credit_routes = [credit_router, credit_admin_router]

credit_router = APIRouter()

for route in credit_routes:
    credit_router.include_router(
        route,
        prefix="/v1/credit"
    )
