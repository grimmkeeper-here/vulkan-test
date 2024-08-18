import redis
from redis.typing import ResponseT
from redlock import Lock, Redlock

from src.config import settings


class RedisClient:
    def __init__(self):
        self.redis_host = settings.redis_host
        self.redis_port = settings.redis_port
        self.redis_db = settings.redis_db
        self.client = redis.Redis(
            host=self.redis_host, port=self.redis_port, db=self.redis_db
        )
        self.dlm = Redlock(
            [{"host": self.redis_host, "port": self.redis_port, "db": self.redis_db}]
        )

    def get(self, key) -> ResponseT:
        return self.client.get(key)

    def set(self, key, value, ex=None):
        self.client.set(key, value, ex=ex)

    def delete_by_pattern(self, pattern):
        """
        Delete keys by pattern
        """
        for key in self.client.scan_iter(match=pattern):
            self.client.delete(key)

    def acquire_lock(self, key, ttl) -> Lock:
        return self.dlm.lock(key, ttl)

    def release_lock(self, lock):
        self.dlm.unlock(lock)
