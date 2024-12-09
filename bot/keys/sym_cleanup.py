import asyncio
import json
import logging

from bot.core.redis_client import get_redis_client
from bot.keys.sym_handler import stop_sym_handler

logger = logging.getLogger("SYM_CLEANUP")

redis_client = get_redis_client()


async def sym_listener_cleaner(inviter_id: int):
    """Starts the listener task."""
    cleaner_task = asyncio.create_task(sym_notifications_listener_cleanup(inviter_id))
    return cleaner_task


async def stop_redis_subscription(redis_sub, inviter_id):
    channel_name = f"conversation:notifications:{inviter_id}"

    await redis_sub.unsubscribe(channel_name)
    await redis_sub.close()

    msg = f"Unsubscribed from {channel_name} and closed the subscription."
    logger.info(msg)


async def sym_notifications_listener_cleanup(inviter_id: int):
    """Listens for notifications and stops when instructed."""
    channel_name = f"conversation:notifications:{inviter_id}"
    redis_sub = redis_client.pubsub()
    await redis_sub.subscribe(channel_name)

    msg = f"Cleanup manager for channel_name {channel_name} listener started."
    logger.info(msg)

    async for message in redis_sub.listen():
        if message["type"] == "message":
            try:
                d = json.loads(message["data"])
                status = d["event"]

                if status == "key_received":
                    await stop_sym_handler(inviter_id=inviter_id)
                    break

            except Exception as e:
                msg = f"Error processing message: {e}"
                logger.exception(msg)

    # Unsubscribe and cleanup
    await stop_redis_subscription(redis_sub=redis_sub, inviter_id=inviter_id)
