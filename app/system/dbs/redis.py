import os

from redis import Redis

redis_client = Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=int(os.environ.get('REDIS_PORT', "6379")),
    db=int(os.environ.get('WALLPAY_REDIS_DB', "2")),
)


class BaseRedis(Redis):
    def __init__(self, host: str = os.environ.get('REDIS_HOST', '127.0.0.1'),
                 port: int = os.environ.get('REDIS_PORT', 6379), db: int = os.environ.get('WALLPAY_REDIS_DB', 2),
                 password=None, socket_timeout=None):
        super().__init__(host=host, port=port, db=db, password=password, socket_timeout=socket_timeout)
