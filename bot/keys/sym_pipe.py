from bot.keys.sym_cleanup import sym_listener_cleaner
from bot.keys.sym_handler import start_sym_handler


async def sym_exchange_cycle(inviter_id: int):
    close_sym_listener = sym_listener_cleaner(inviter_id)
    if close_sym_listener:
        await close_sym_listener

    sym_notification_listener = await start_sym_handler(inviter_id)
    if sym_notification_listener:
        await sym_notification_listener
