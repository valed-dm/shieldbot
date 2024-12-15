from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.core.bot_instance import get_bot_instance
from bot.keyboards.button_confirm import confirm_button
from bot.keys.key_status import notify_key_received
from bot.utils.user_data_resolver import UserDataResolver

bot = get_bot_instance()


async def on_invitee_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """Invitee input processing after '🔒 @Username' button click."""
    inviter = UserDataResolver(callback_query)
    secure_id, invitee_id, invitee_username = callback_query.data.split(":")[1:]

    await state.update_data(
        secure_id=secure_id,
        inviter_id=inviter.id,
        invitee_id=invitee_id,
    )

    await notify_key_received(inviter.id, secure_id)

    callback_conversation_data = f"ie:{secure_id}:{inviter.id}:{invitee_id}"

    confirm_start = confirm_button(callback_conversation_data)
    await bot.send_message(
        chat_id=invitee_id,
        text=f"✅ {inviter.username} is waiting for 🔒SecureTalk to be accepted",
        reply_markup=confirm_start,
    )

    await callback_query.message.answer(
        f"✅ Waiting for 🔒SecureTalk to be accepted by: "
        f"{invitee_username}: id[{invitee_id}]",
    )
