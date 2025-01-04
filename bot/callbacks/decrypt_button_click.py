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
    """Handle 'SecureTalk Decrypt' button clicks for both inviter and invitee."""
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
