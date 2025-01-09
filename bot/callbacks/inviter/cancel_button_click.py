"""Cancel button click callback handler."""

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
    """
    Handles 'Cancel' button clicks to reset SecureTalk data on the inviter's side.

    This function verifies the callback data, clears the SecureTalk state prepared
    on the inviter's side, and notifies the user about the cancellation.

    :param callback_query: The callback query triggered by the 'Cancel' button.
    :type callback_query: types.CallbackQuery
    :param state: The FSMContext to manage and reset the conversation state.
    :type state: FSMContext

    :raises ValueError: If the callback verification fails, logs the error
                            and notifies the user via an alert.

    :return: None
    """
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
