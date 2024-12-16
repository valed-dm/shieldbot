from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv

from bot.core.bot_instance import get_bot_instance
from bot.core.state import FSMStateManager
from bot.core.user_data_resolver import UserDataResolver
from bot.keyboards.inviter_contacts_keyboard import contacts_keyboard
from bot.keyboards.main_menu_keyboard import main_menu_keyboard
from bot.keys.aes.sym_pipe import sym_exchange_cycle
from bot.utils.invitee.resolve_invitation import resolve_invitation
from bot.utils.invitee.store_invitee import store_invitee
from bot.utils.inviter.inviter_workflow import initialize_inviter_workflow

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

            fsm_manager = FSMStateManager(state)
            await fsm_manager.load()

            fsm_manager.secure_id = secure_id
            fsm_manager.inviter_id = inviter_id
            fsm_manager.invitee_id = user.id

            await fsm_manager.save()

            contacts, contacts_qty = await contacts_keyboard(
                int(inviter_id),
                inviter_username,
            )
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
