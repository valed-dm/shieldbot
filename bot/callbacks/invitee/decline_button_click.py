"""Decline button click callback handler."""

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
    """
    Handles the 'Decline' button click event for an invitee.

    This function processes the invitee's decision to decline an invitation by:
    - Verifying callback data.
    - Resetting the SecureTalk state on the invitee's side.
    - Notifying the inviter about the declined invitation.
    - Providing the inviter with an option to cancel the SecureTalk session.

    :param callback_query: The callback query triggered by the 'Decline' button.
    :type callback_query: types.CallbackQuery
    :param state: The current finite state machine (FSM) context.
    :type state: FSMContext

    :raises ValueError: If callback data verification fails.

    :return: None
    """
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
