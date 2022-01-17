import redis
from typing import Any

redis_conn = redis.Redis(host="localhost", port=6379, db=0)


class Redis:
    @staticmethod
    def set(key: str, value: Any):
        return redis_conn.set(key, value, ex=7 * 24 * 3600)

    @staticmethod
    def expire(key: str, time: int):
        return redis_conn.expire(key, time)

    @staticmethod
    def delete(key: str):
        return redis_conn.delete(key)
