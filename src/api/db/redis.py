import redis
from typing import Any


class Redis:
    def __init__(self, db: int = 0):
        pool = redis.ConnectionPool(host="localhost", port=6379, db=db)
        self.conn = redis.Redis(connection_pool=pool)

    def set(self, key: str, value: Any, ex: int = 7 * 24 * 3600):
        return self.conn.set(key, value, ex)

    def expire(self, key: str, time: int):
        return self.conn.expire(key, time)

    def delete(self, key: str):
        return self.conn.delete(key)

    def get(self, key: str):
        v = self.conn.get(key)

        if v:
            v = v.decode()

        return v


default_redis_db = Redis(0)
