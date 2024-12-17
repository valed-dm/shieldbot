import hashlib

from bot.core.redis_client import get_redis_client

redis_client = get_redis_client()

TTL = 3600


async def store_callback_data(*args):
    """
    Stores the full data in Redis with the reference ID as the key.
    """
    raw_data = ":".join(map(str, args))
    reference_id = hashlib.sha256(raw_data.encode()).hexdigest()[:16]

    await redis_client.setex(reference_id, TTL, raw_data)

    return reference_id


async def get_callback_data(reference_id):
    """
    Retrieves the full data from Redis using the reference ID.
    """
    data = await redis_client.get(reference_id)
    if data is None:
        msg = "Reference ID has expired or is invalid!"
        raise ValueError(msg)
    return data


async def create_callback_data(prefix: str, *args) -> str:
    """
    Gracefully creates callback data by prefixing it and appending stored data.
    """
    reference_id = await store_callback_data(*args)

    return f"{prefix}{reference_id}"
