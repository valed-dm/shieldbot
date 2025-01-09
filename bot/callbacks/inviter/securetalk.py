"""SecureTalk button click callback handler."""

import logging
import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.callbacks.data.callback_controller import CallbackController
from bot.core.bot_instance import get_bot_instance
from bot.keyboards.button_invite import invite_button
from bot.keyboards.inviter_contacts_keyboard import contacts_keyboard

load_dotenv()

logger = logging.getLogger("SECURETALK_BUTTON")

bot = get_bot_instance()
LOGO = os.getenv("LOGO")


async def on_prepare_secure_talk(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    callback = CallbackController(callback_query, state, bot)

    try:
        if not await callback.callback_controller(
            expected_prefix="ir:prepare:",
            params_count=0,
        ):
            return

    except ValueError as e:
        msg = f"Callback verification failed: {e}"
        logger.exception(msg)
        await callback_query.answer(str(e), show_alert=True)

    contacts_markup, contacts_qty = await contacts_keyboard(
        callback.sender.id,
        callback.sender.username,
    )

    text_invite = (
        f"Invite a partner for {LOGO} from the list;\n"
        f"Use 'Settings:Invite partner' if empty."
    )

    if contacts_qty != 0:
        await callback_query.message.answer(
            text_invite,
            reply_markup=contacts_markup,
        )
    else:
        invite_partner_keyboard = invite_button()
        await callback_query.message.answer(
            f"No active {LOGO}s. Invite a partner.",
            reply_markup=invite_partner_keyboard,
        )
