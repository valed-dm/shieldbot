from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv

from bot.core.bot_instance import get_bot_instance
from bot.keyboards.inviter_contacts_keyboard import contacts_keyboard
from bot.keyboards.main_menu_keyboard import main_menu_keyboard
from bot.keys.sym_pipe import sym_exchange_cycle
from bot.utils.inviter_workflow import initialize_inviter_workflow
from bot.utils.resolve_invitation import resolve_invitation
from bot.utils.store_invitee import store_invitee
from bot.utils.user_data_resolver import UserDataResolver

if TYPE_CHECKING:
    from aiogram import types
    from aiogram.fsm.context import FSMContext

load_dotenv()

logger = logging.getLogger("START_COMMAND")

bot = get_bot_instance()
LOGO = os.getenv("LOGO")


async def start_command(message: types.Message, state: FSMContext):
    text = message.text
    user = UserDataResolver(message)

    if len(text.split()) > 1:
        # Invitee's side deep link processing operations
        inviter_id: str | None = None
        inviter_username: str | None = None

        secure_id = text.split()[1]

        msg = f"Invitation handling for {LOGO} '{user.username}' started"
        logger.info(msg)

        try:
            inviter_id, inviter_username = await resolve_invitation(
                secure_id,
                user.id,
            )
        except Exception as e:
            msg = f"Invitation is not resolved for {LOGO} '{user.username}': {e}"
            logger.exception(msg)
            await message.answer(
                f"An error {e} occurred while resolving {LOGO} '{user.username}' "
                f"invitation. Please try again.",
            )

        if inviter_id:
            await store_invitee(secure_id, user)

            await state.update_data(
                secure_id=secure_id,
                inviter_id=int(inviter_id),
                invitee_id=user.id,
            )

            contacts, contacts_qty = await contacts_keyboard(int(inviter_id))
            await bot.send_message(
                inviter_id,
                f"Press button '{user.username}' to start {LOGO} conversation",
                reply_markup=contacts,
            )
            await bot.send_message(
                user.id,
                f"Now waiting for {LOGO} with '{inviter_username}' to start",
            )

            msg = (
                f"{LOGO} {inviter_username} invitation resolved successfully: "
                f"{user.id}:'{user.username}'"
            )
            logger.info(msg)
        else:
            msg = (
                f"{LOGO} '{inviter_username}' invalid or expired invitation: "
                f"{user.id}:'{user.username}'"
            )
            logger.warning(msg)
            await message.answer(f"Invalid or expired {LOGO} invitation link.")
    else:
        # Inviter's side preparing operations
        try:
            await initialize_inviter_workflow(user.id)
            msg = f"RSA key pair for {LOGO} '{user.username}' is prepared."
            logger.info(msg)
        except Exception as e:
            msg = f"Error initializing RSA keys for {LOGO} '{user.username}': {e}"
            logger.exception(msg)
            await message.answer(
                f"An error occurred while setting up {LOGO}. Please try again.",
            )

        await message.answer(
            f"Welcome to {LOGO}! Choose an action below:",
            reply_markup=main_menu_keyboard,
        )

        await sym_exchange_cycle(user.id)
