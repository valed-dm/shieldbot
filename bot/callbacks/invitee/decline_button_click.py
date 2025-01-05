import logging
import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.callbacks.data.callback_controller import CallbackController
from bot.core.bot_instance import get_bot_instance
from bot.keyboards.button_cancel import cancel_button

load_dotenv()

logger = logging.getLogger("DECLINE_BUTTON")

bot = get_bot_instance()
LOGO = os.getenv("LOGO")


async def on_decline_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """Drop SecureTalk data prepared on invitee's side
    to default empty state on 'Decline' button click."""
    callback = CallbackController(callback_query, state, bot)

    try:
        if not await callback.callback_controller(
            expected_prefix="ie:decline:",
            params_count=5,
        ):
            return
        await callback.abort_securetalk_state()

    except ValueError as e:
        msg = f"Callback verification failed: {e}"
        logger.exception(msg)
        await callback_query.answer(str(e), show_alert=True)

    msg = (
        f"{LOGO} @{callback.inviter_username} "
        f"invitation declined by @{callback.invitee_username}!"
    )

    inviter_callback_cancel_securetalk = f"ir:cancel:{callback.reference_id}"
    cancel_keyboard = cancel_button(inviter_callback_cancel_securetalk)

    await bot.send_message(
        chat_id=callback.inviter_id,
        text=msg,
        reply_markup=cancel_keyboard,
    )
    await callback_query.message.answer(msg)
