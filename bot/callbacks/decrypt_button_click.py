"""Abort button click callback handler."""

import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.callbacks.data.callback_controller import CallbackController
from bot.core.bot_instance import get_bot_instance
from bot.messages.handlers.on_decrypt import decrypt_text

logger = logging.getLogger("DECRYPT_BUTTON")

bot = get_bot_instance()


async def on_decrypt_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    expected_prefix: str,
):
    """
    Handle 'SecureTalk Decrypt' button clicks for both inviter and invitee.

    This function processes the decryption workflow triggered by the 'Decrypt' button.
    It verifies the callback data, loads the required SecureTalk state, decrypts the
    secure message, and sends the decrypted text back to the user.

    :param callback_query: The callback query object triggered by the button click.
    :type callback_query: types.CallbackQuery
    :param state: The FSM context for storing and retrieving state data.
    :type state: FSMContext
    :param expected_prefix: The expected prefix for the callback to verify its validity.
    :type expected_prefix: str

    :raises ValueError: If the callback verification fails or the data is invalid.

    Workflow:
        1. Validates the callback data against the expected prefix.
        2. Loads the SecureTalk state to retrieve encryption-related details.
        3. Decrypts the secure message and identifies the sender.
        4. Sends the decrypted message to the user who triggered the callback.

    Example response to the user:
        `@sender: Decrypted message content`

    Error Handling:
        - If the callback data is invalid or verification fails, logs the exception
          and displays an alert to the user with the relevant error message.
    """
    callback = CallbackController(callback_query, state, bot)
    decrypted_text = ""
    sender = ""

    try:
        if not await callback.callback_controller(
            expected_prefix=expected_prefix,
            params_count=1,
        ):
            return

        await callback.load_securetalk_state()
        decrypted_text, sender = await decrypt_text(callback)

    except ValueError as e:
        msg = f"Callback verification failed: {e}"
        logger.exception(msg)
        await callback_query.answer(str(e), show_alert=True)

    msg = f"@{sender}: {decrypted_text}"

    await callback_query.message.answer(msg)
