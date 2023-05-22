"""Modules providingFunctions"""
import dataclasses
import os

from celery import Celery

from .setup import router

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/1")


@dataclasses.dataclass
class Config:
    """
    we keep celery main app configuration params in this clas
    """

    broker_url = CELERY_BROKER_URL
    result_backend = CELERY_RESULT_BACKEND
    enable_utc = True
    task_track_started = True
    send_task_events = True
    imports = router.imports()
    task_default_queue = "wallpay-tasks"
    task_routes = router.routes()


app = Celery("wallpay-celery")
app.config_from_object(Config)
