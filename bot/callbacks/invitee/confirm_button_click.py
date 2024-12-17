import logging
import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.callbacks.data.callback_verify import CallbackVerifier
from bot.core.bot_instance import get_bot_instance

load_dotenv()

logger = logging.getLogger("CONFIRM_BUTTON")

bot = get_bot_instance()
LOGO = os.getenv("LOGO")


async def on_confirm_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """Invitee state updating after 'Confirm ' button click."""
    verifier = CallbackVerifier(callback_query, state, "invitee")

    try:
        if not await verifier.verify(expected_prefix="ie:", params_count=5):
            return
        await verifier.update_state()

    except ValueError as e:
        msg = f"Callback verification failed: {e}"
        logger.exception(msg)
        await callback_query.answer(str(e), show_alert=True)

    msg = (
        f"{LOGO} '{verifier.inviter_username}✅{verifier.invitee_username}' is active!"
    )
    await bot.send_message(
        chat_id=verifier.inviter_id,
        text=msg,
    )
    await callback_query.message.answer(msg)
