from fastapi import APIRouter

from .v1.api import notification_route

notification_routes = [notification_route]

notification_router = APIRouter()

for route in notification_routes:
    notification_router.include_router(
        route,
        prefix="/v1/notification",
    )
