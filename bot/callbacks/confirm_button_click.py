from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.core.bot_instance import get_bot_instance

bot = get_bot_instance()


async def on_confirm_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """Invitee state updating after 'Confirm ' button click."""
    secure_id, inviter_id, invitee_id = callback_query.data.split(":")[1:]
    msg = "✅ 🔒SecureTalk is active!"

    await state.update_data(
        secure_id=secure_id,
        inviter_id=inviter_id,
        invitee_id=invitee_id,
    )

    await bot.send_message(
        chat_id=inviter_id,
        text=msg,
    )
    await callback_query.message.answer(msg)
