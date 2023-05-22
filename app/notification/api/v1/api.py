from fastapi import APIRouter

from ..v1.endpoints import center

notification_route = APIRouter()

notification_route.include_router(
    center.router,
    prefix='/center',
    tags=['notification']
)
