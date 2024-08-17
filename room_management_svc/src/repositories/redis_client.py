import redis
from redis.typing import ResponseT

from src.config import settings


class RedisClient:
    def __init__(self):
        self.redis_host = settings.redis_host
        self.redis_port = settings.redis_port
        self.redis_db = settings.redis_db
        self.client = redis.Redis(
            host=self.redis_host, port=self.redis_port, db=self.redis_db
        )

    def get(self, key) -> ResponseT:
        return self.client.get(key)

    def set(self, key, value, ex=None):
        self.client.set(key, value, ex=ex)
