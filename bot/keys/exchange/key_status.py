import json

from bot.core.redis_client import get_redis_client

redis_client = get_redis_client()


async def notify_key_ready(inviter_id: int, secure_id: str):
    """Notify the inviter that the encrypted symmetric key is ready."""
    message = {
        "data": secure_id,
        "inviter_id": inviter_id,
        "event": "key_ready",
    }
    await redis_client.publish(
        f"conversation:notifications:{inviter_id}",
        json.dumps(message),
    )


async def notify_key_received(inviter_id: int, secure_id: str):
    """Notify the inviter that the encrypted symmetric key is ready."""
    message = {
        "data": secure_id,
        "inviter_id": inviter_id,
        "event": "key_received",
    }
    await redis_client.publish(
        f"conversation:notifications:{inviter_id}",
        json.dumps(message),
    )
