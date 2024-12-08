"""Singleton module for Redis client."""

from functools import lru_cache

from redis.asyncio import Redis


@lru_cache(maxsize=1)
def get_redis_client() -> Redis:
    """Singleton Redis client instance."""
    return Redis(host="localhost", port=6379, decode_responses=True)
