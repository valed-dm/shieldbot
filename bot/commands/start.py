from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from bot.keyboards.menu_keyboard import main_menu_keyboard
from bot.keys.sym_pipe import sym_exchange_cycle
from bot.utils.inviter_workflow import initialize_inviter_workflow
from bot.utils.resolve_invitation import resolve_invitation
from bot.utils.store_invitee import store_invitee

if TYPE_CHECKING:
    from aiogram import types

logger = logging.getLogger("START_COMMAND")


async def start_command(message: types.Message):
    text = message.text

    # Invitee's side SecureTalkBot operations
    if len(text.split()) > 1:
        success = False
        secure_id = text.split()[1]

        invitee_id = message.from_user.id
        invitee_username = message.from_user.username  # Username
        invitee_first_name = message.from_user.first_name  # First Name
        invitee_last_name = message.from_user.last_name or "not_available"

        msg = f"Resolving invitation: secure_id={secure_id}, invitee_id={invitee_id}"
        logger.info(msg)

        try:
            success = await resolve_invitation(secure_id, invitee_id)
        except Exception as e:
            msg = f"Invitation has not been resolved for invitee_id={invitee_id}: {e}"
            logger.exception(msg)
            await message.answer(
                f"An error {e} occurred while resolving invitation. Please try again.",
            )

        if success:
            await store_invitee(
                secure_id=secure_id,
                partner_id=invitee_id,
                partner_username=invitee_username,
                partner_first_name=invitee_first_name,
                partner_last_name=invitee_last_name,
            )

            await message.answer("You are now connected for secure chat!")

            msg = f"Invitation resolved successfully for invitee_id={invitee_id}"
            logger.info(msg)
        else:
            msg = f"Invalid or expired invitation for invitee_id={invitee_id}"
            logger.warning(msg)
            await message.answer("Invalid or expired invitation link.")

    # Inviter's side SecureTalkBot operations
    else:
        user_id = message.from_user.id

        try:
            await initialize_inviter_workflow(inviter_id=user_id)
            msg = f"RSA key pair for user_id={user_id} created successfully."
            logger.info(msg)
        except Exception as e:
            msg = f"Error initializing RSA keys for user_id={message.from_user.id}: {e}"
            logger.exception(msg)
            await message.answer(
                "An error occurred while setting up your secure chat. "
                "Please try again.",
            )

        await message.answer(
            "Welcome to SecureTalk! Choose an action below:",
            reply_markup=main_menu_keyboard,
        )

        await sym_exchange_cycle(inviter_id=user_id)
