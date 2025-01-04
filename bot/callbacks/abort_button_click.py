import logging
import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.callbacks.data.callback_verify import CallbackVerifier

load_dotenv()

logger = logging.getLogger("CLOSE_BUTTON")

LOGO = os.getenv("LOGO")


async def on_abort_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    expected_prefix: str,
):
    """Handle 'Abort SecureTalk' button clicks for both inviter and invitee."""
    verifier = CallbackVerifier(callback_query, state)
    inviter_username = ""
    invitee_username = ""

    try:
        if not await verifier.verify(expected_prefix=expected_prefix, params_count=1):
            return
        inviter_username, invitee_username = await verifier.abort_conversation_state()

    except ValueError as e:
        msg = f"Callback verification failed: {e}"
        logger.exception(msg)
        await callback_query.answer(str(e), show_alert=True)

    msg = f"{LOGO} @{inviter_username}❌@{invitee_username} aborted!"

    await callback_query.message.answer(msg)
