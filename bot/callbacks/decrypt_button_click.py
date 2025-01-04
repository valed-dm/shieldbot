import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.callbacks.data.callback_verify import CallbackVerifier

logger = logging.getLogger("DECRYPT_BUTTON")


async def on_decrypt_button_click(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    expected_prefix: str,
):
    """Handle 'SecureTalk Decrypt' button clicks for both inviter and invitee."""
    verifier = CallbackVerifier(callback_query, state)
    decrypted_text = ""
    sender = ""

    try:
        if not await verifier.verify(expected_prefix=expected_prefix, params_count=1):
            return
        decrypted_text, sender = await verifier.decrypt_text()

    except ValueError as e:
        msg = f"Callback verification failed: {e}"
        logger.exception(msg)
        await callback_query.answer(str(e), show_alert=True)

    msg = f"@{sender}: {decrypted_text}"

    await callback_query.message.answer(msg)
