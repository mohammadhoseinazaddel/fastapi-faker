from typing import List

from .router import TaskRouter


modules: List[str] = [
    'credit',
    'ext_services',
    'finance',
    'notification',
    'order',
    'system_object',
    'user',
    'user_assets',
]

router = TaskRouter(modules)
