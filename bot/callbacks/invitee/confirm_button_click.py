"""Confirm button click callback handler."""

import logging
import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.callbacks.data.callback_controller import CallbackController
from bot.core.bot_instance import get_bot_instance

load_dotenv()

logger = logging.getLogger("CONFIRM_BUTTON")

bot = get_bot_instance()
LOGO = os.getenv("LOGO")


async def on_confirm_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
) -> None:
    """
    Handles the 'Confirm' button click event for an invitee.

    This function verifies and processes callback data for the invitee's confirmation
    action. If the callback data verification passes, it updates the invitee's
    SecureTalk state and sends notifications to both the inviter and invitee.

    :param callback_query: The callback query triggered by the 'Confirm' button.
    :type callback_query: types.CallbackQuery
    :param state: The current finite state machine (FSM) context.
    :type state: FSMContext

    :raises ValueError: If callback data verification fails.

    :return: None
    """
    callback = CallbackController(callback_query, state, bot)

    try:
        if not await callback.callback_controller(
            expected_prefix="ie:accept:",
            params_count=5,
        ):
            return
        await callback.set_securetalk_state()

    except ValueError as e:
        msg = f"Callback verification failed: {e}"
        logger.exception(msg)
        await callback_query.answer(str(e), show_alert=True)

    msg = (
        f"{LOGO} @{callback.inviter_username}✅@{callback.invitee_username} is active!"
    )
    await bot.send_message(
        chat_id=callback.inviter_id,
        text=msg,
    )
    await callback_query.message.answer(msg)
