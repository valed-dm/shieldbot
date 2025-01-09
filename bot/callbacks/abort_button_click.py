"""Abort button click callback handler."""

import logging
import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.callbacks.data.callback_controller import CallbackController
from bot.core.bot_instance import get_bot_instance

load_dotenv()

logger = logging.getLogger("ABORT_BUTTON")

LOGO = os.getenv("LOGO")

bot = get_bot_instance()


async def on_abort_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    expected_prefix: str,
):
    """
    Handles 'Abort SecureTalk' button clicks for both inviter and invitee.

    This function verifies the callback data, aborts the SecureTalk state, and
    notifies the user about the abortion with an appropriate message.

    :param callback_query: The callback query triggered by the abort button.
    :type callback_query: types.CallbackQuery
    :param state: The FSMContext to manage and retrieve conversation states.
    :type state: FSMContext
    :param expected_prefix: The expected prefix for the callback data to
                               validate its structure.
    :type expected_prefix: str

    :raises ValueError: If the callback verification fails, a descriptive error
                           is logged, and the user is notified via an alert.

    :return: None
    """

    callback = CallbackController(callback_query, state, bot)
    inviter_username = ""
    invitee_username = ""

    try:
        if not await callback.callback_controller(
            expected_prefix=expected_prefix,
            params_count=1,
        ):
            return
        inviter_username, invitee_username = await callback.abort_securetalk_state()

    except ValueError as e:
        msg = f"Callback verification failed: {e}"
        logger.exception(msg)
        await callback_query.answer(str(e), show_alert=True)

    msg = f"{LOGO} @{inviter_username}❌@{invitee_username} aborted!"

    await callback_query.message.answer(msg)
