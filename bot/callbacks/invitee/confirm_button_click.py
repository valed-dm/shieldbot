from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.callbacks.data.redis_reference import get_callback_data
from bot.core.bot_instance import get_bot_instance
from bot.core.state import FSMStateManager
from bot.core.user_data_resolver import UserDataResolver

bot = get_bot_instance()


async def on_confirm_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """Invitee state updating after 'Confirm ' button click."""
    if not callback_query.data.startswith("ie:"):
        await callback_query.answer("❌ Invalid callback data!")
        return

    invitee = UserDataResolver(callback_query)

    _, reference_id = callback_query.data.split(":")
    data = await get_callback_data(reference_id)

    secure_id, inviter_id, inviter_username, invitee_id, invitee_username = data.split(
        ":",
    )

    if str(invitee.id) != invitee_id:
        await callback_query.answer("❌ Invitation data corrupted!", show_alert=True)
        return

    msg = f"✅ {inviter_username}/{invitee_username} 🔒SecureTalk is active!"

    fsm_manager = FSMStateManager(state)
    await fsm_manager.load()

    fsm_manager.secure_id = secure_id
    fsm_manager.inviter_id = inviter_id
    fsm_manager.invitee_id = invitee_id

    await fsm_manager.save()

    await bot.send_message(
        chat_id=inviter_id,
        text=msg,
    )
    await callback_query.message.answer(msg)
