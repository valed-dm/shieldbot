"""Singleton Redis client module."""

import os
from functools import lru_cache

from redis.asyncio import Redis


@lru_cache(maxsize=1)
def get_redis_client() -> Redis:
    """
    Singleton Redis client instance.

    Returns:
        Redis: An instance of the Redis client configured to connect to the server.

    Notes:
        - Uses @lru_cache to ensure only one instance is created and reused.
        - Host and port are configurable via environment variables.
        - Decodes responses by default for easier usage.

    Raises:
        redis.exceptions.RedisError: If the Redis server is unreachable or
        misconfigured.
    """
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))

    try:
        client = Redis(host=host, port=port, decode_responses=True)
        # Optional: Add a ping or a check to ensure connection validity
    except Exception as e:
        exc_msg = f"Failed to initialize Redis client: {e}"
        raise RuntimeError(exc_msg) from e
    else:
        return client


async def close_redis_client():
    """
    Closes the Redis client instance if it exists.
    """
    client = get_redis_client()
    if client:
        await client.close()
