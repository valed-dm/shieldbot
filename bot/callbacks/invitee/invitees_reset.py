from aiogram import types

from bot.core.redis_client import get_redis_client
from bot.keyboards.main_menu_keyboard import main_menu_keyboard

redis_client = get_redis_client()


async def on_reset_invitees(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await redis_client.delete(f"inviter_conversations:{user_id}")
    await callback_query.message.answer(
        "✅ All your previous conversations are cleaned up!",
        reply_markup=main_menu_keyboard,
    )
