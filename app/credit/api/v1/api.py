from fastapi import APIRouter

from .endpoints import user, score, credit_admin, credit_levels

credit_router = APIRouter()
credit_admin_router = APIRouter()

credit_router.include_router(
    user.router,
    prefix='/user',
    tags=['credit']
)

credit_router.include_router(
    score.router,
    prefix='/score',
    tags=['credit']
)

credit_router.include_router(
    credit_levels.router,
    prefix="/levels",
    tags=['credit'],
)

credit_admin_router.include_router(
    credit_admin.router,
    prefix='/admin',
    tags=['credit-admin']
)
