import asyncio
import contextlib
import json
import logging

from bot.core.redis_client import get_redis_client
from bot.keys.key_listen import listen_for_notifications

logger = logging.getLogger("SYM_HANDLER")
redis_client = get_redis_client()

sym_notification_tasks = {}


async def start_sym_handler(inviter_id: int):
    # Check if a task already exists for this inviter_id
    if inviter_id in sym_notification_tasks:
        logging.info("You are already being listened to!")
        return None

    logging.info("Launch Symmetric Key listener.")

    notification_task = asyncio.create_task(
        listen_for_notifications(inviter_id=inviter_id),
    )
    sym_notification_tasks[inviter_id] = notification_task

    return notification_task


async def stop_redis_subscription(redis_sub, inviter_id):
    channel_name = f"conversation:notifications:{inviter_id}"

    await redis_sub.unsubscribe(channel_name)
    await redis_sub.close()

    msg = f"Unsubscribed from {channel_name} and closed the subscription."
    logging.info(msg)


async def stop_sym_handler(inviter_id: int):
    if inviter_id in sym_notification_tasks:
        task = sym_notification_tasks.pop(inviter_id)
        task.cancel()
        msg = f"symmetric key notification task for {inviter_id} successfully finished"
        logging.info(msg)
        with contextlib.suppress(asyncio.CancelledError):
            await task
        logging.info("Stopped listening for notifications.")
    else:
        logging.info("No listener running for you!")


async def close_sym_notifications_listener(inviter_id: int):
    """Listens for notifications and stops when instructed."""
    redis_sub = redis_client.pubsub()
    await redis_sub.subscribe(f"conversation:notifications:{inviter_id}")

    msg = f"Closing listener for inviter_id={inviter_id} symmetric key cycle started."
    logging.info(msg)

    async for message in redis_sub.listen():
        if message["type"] == "message":
            try:
                d = json.loads(message["data"])
                status = d["event"]

                if status == "key_received":
                    # Call your stop handler
                    await stop_sym_handler(inviter_id=inviter_id)

                    # Notify that processing is complete
                    msg = f"Key processing complete for inviter_id={inviter_id}."
                    logging.info(msg)

                    # Exit listener
                    break
            except Exception as e:
                msg = f"Error processing message: {e}"
                logging.exception(msg)

    # Unsubscribe and cleanup
    await stop_redis_subscription(redis_sub=redis_sub, inviter_id=inviter_id)
    msg = f"Listener for inviter_id={inviter_id} stopped."
    logging.info(msg)


async def start_close_sym_listener(inviter_id: int):
    """Starts the listener task."""
    task = asyncio.create_task(close_sym_notifications_listener(inviter_id))
    return task
