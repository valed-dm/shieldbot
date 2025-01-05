import logging
import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.callbacks.data.callback_controller import CallbackController
from bot.core.bot_instance import get_bot_instance

load_dotenv()

logger = logging.getLogger("CANCEL_BUTTON")

bot = get_bot_instance()
LOGO = os.getenv("LOGO")


async def on_cancel_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """Drop SecureTalk data prepared on inviter's side
    to default empty state on 'Cancel' button click."""
    callback = CallbackController(callback_query, state, bot)

    try:
        if not await callback.callback_controller(
            expected_prefix="ir:cancel:",
            params_count=5,
        ):
            return
        await callback.abort_securetalk_state()

    except ValueError as e:
        msg = f"Callback verification failed: {e}"
        logger.exception(msg)
        await callback_query.answer(str(e), show_alert=True)

    msg = f"{LOGO} invitation has been successfully cancelled!"

    await callback_query.message.answer(msg)
