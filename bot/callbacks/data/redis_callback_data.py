import hashlib
import logging

import redis

from bot.core.redis_client import get_redis_client

redis_client = get_redis_client()

TTL = 3600

logger = logging.getLogger("REDIS_CALLBACK_DATA_STORAGE")


async def store_callback_data(*args):
    """
    Stores the full data in Redis with the reference ID as the key.

    Args:
        *args: Arbitrary arguments that represent the callback data to be stored.

    Returns:
        str: The generated reference ID, which acts as the key for retrieving the
        stored data.

    Raises:
        redis.exceptions.RedisError: If an error occurs while setting data in Redis.
    """
    raw_data = ":".join(map(str, args))
    reference_id = hashlib.sha256(raw_data.encode()).hexdigest()[:16]

    try:
        await redis_client.setex(reference_id, TTL, raw_data)
    except redis.exceptions.RedisError as e:
        logger.exception("Failed to store callback data in Redis.")
        exc_msg = "Failed to store callback data."
        raise RuntimeError(exc_msg) from e

    return reference_id


async def get_callback_data(reference_id):
    """
    Retrieves the full data from Redis using the reference ID.

    Args:
        reference_id (str): The unique identifier for retrieving stored callback data.

    Returns:
        str: The stored callback data associated with the reference ID.

    Raises:
        ValueError: If the reference ID is invalid or the data has expired.
        redis.exceptions.RedisError: If an error occurs while retrieving data
        from Redis.
    """
    data = await redis_client.get(reference_id)
    if data is None:
        msg = "Reference ID has expired or is invalid!"
        raise ValueError(msg)
    return data


async def create_callback_data(prefix: str, *args) -> str:
    """
    Gracefully creates callback data by prefixing it and appending stored data.

    Args:
        prefix (str): A prefix string to be added to the callback data (e.g., "cb_").
        *args: Arbitrary arguments representing the data to be included in the callback.

    Returns:
        str: The formatted callback data string, including the prefix and reference ID.

    Raises:
        redis.exceptions.RedisError: If an error occurs during the storage of
        callback data.
    """
    reference_id = await store_callback_data(*args)

    return f"{prefix}{reference_id}"
