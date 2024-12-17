import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.callbacks.data.redis_reference import get_callback_data
from bot.core.bot_instance import get_bot_instance
from bot.core.state import FSMStateManager
from bot.core.user_data_resolver import UserDataResolver
from bot.keyboards.button_confirm import confirm_button
from bot.keys.exchange.key_status import notify_key_received

load_dotenv()
bot = get_bot_instance()

LOGO = os.getenv("LOGO")


async def on_invitee_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """Invitee input processing after '🔒 @Username' button click."""
    if not callback_query.data.startswith("ir:"):
        await callback_query.answer("❌ Invalid callback data!")
        return

    inviter = UserDataResolver(callback_query)

    _, reference_id = callback_query.data.split(":")

    data = await get_callback_data(reference_id)
    secure_id, inviter_id, inviter_username, invitee_id, invitee_username = data.split(
        ":",
    )

    if str(inviter.id) != inviter_id:
        await callback_query.answer("❌ Invitation data corrupted", show_alert=True)
        return

    fsm_manager = FSMStateManager(state)
    await fsm_manager.load()

    fsm_manager.secure_id = secure_id
    fsm_manager.inviter_id = inviter_id
    fsm_manager.invitee_id = invitee_id

    await fsm_manager.save()

    await notify_key_received(inviter.id, secure_id)

    invitee_callback_confirm_conversation_data = f"ie:{reference_id}"

    confirm_start = confirm_button(invitee_callback_confirm_conversation_data)
    await bot.send_message(
        chat_id=invitee_id,
        text=f"'{inviter_username}' is waiting for {LOGO} to be confirmed.",
        reply_markup=confirm_start,
    )

    await callback_query.message.answer(
        f"Waiting for '{invitee_username}' {LOGO} confirmation...",
    )
