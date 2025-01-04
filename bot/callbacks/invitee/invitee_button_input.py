import logging
import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.callbacks.data.callback_controller import CallbackController
from bot.core.bot_instance import get_bot_instance
from bot.keyboards.button_confirm import confirm_button
from bot.keys.exchange.key_status import notify_key_received

load_dotenv()

logger = logging.getLogger("CONFIRM_BUTTON")

bot = get_bot_instance()
LOGO = os.getenv("LOGO")


async def on_invitee_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """Invitee input processing on '🔒 @Username' button click."""
    callback = CallbackController(callback_query, state, bot)

    try:
        if not await callback.callback_controller(
            expected_prefix="ir:invite:",
            params_count=5,
        ):
            return
        await callback.set_securetalk_state()

    except ValueError as e:
        msg = f"Callback verification failed: {e}"
        logger.exception(msg)
        await callback_query.answer(str(e), show_alert=True)

    await notify_key_received(callback.inviter_id, callback.secure_id)

    invitee_callback_confirm_conversation_data = f"ie:accept:{callback.reference_id}"
    confirm_start = confirm_button(invitee_callback_confirm_conversation_data)

    await bot.send_message(
        chat_id=callback.invitee_id,
        text=f"@{callback.inviter_username} is waiting for {LOGO} to be confirmed.",
        reply_markup=confirm_start,
    )

    await callback_query.message.answer(
        f"Waiting for @{callback.invitee_username} confirmation..",
    )
