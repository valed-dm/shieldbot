import asyncio
import contextlib
import logging

from bot.keys.exchange.key_listen import listen_for_sym_notifications

logger = logging.getLogger("SYM_HANDLER")

sym_notification_tasks = {}


async def start_sym_handler(inviter_id: int):
    if inviter_id in sym_notification_tasks:
        logger.info("You are already being listened to!")
        return None

    sym_notification_task = asyncio.create_task(
        listen_for_sym_notifications(inviter_id),
    )
    sym_notification_tasks[inviter_id] = sym_notification_task

    return sym_notification_task


async def stop_sym_handler(inviter_id: int):
    if inviter_id in sym_notification_tasks:
        task = sym_notification_tasks.pop(inviter_id)
        task.cancel()

        with contextlib.suppress(asyncio.CancelledError):
            await task
    else:
        logger.info("No listener running for you!")
