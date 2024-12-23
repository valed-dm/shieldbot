from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv

from bot.core.bot_instance import get_bot_instance
from bot.core.redis_client import get_redis_client
from bot.core.state import FSMStateManager
from bot.core.user_data_resolver import UserDataResolver
from bot.keyboards.inviter_contacts_keyboard import contacts_keyboard
from bot.messages.invitee.invitee_deeplink import invitation_link_created_message
from bot.utils.invitee.resolve_invitee import resolve_invitee

if TYPE_CHECKING:
    from aiogram import types
    from aiogram.fsm.context import FSMContext

load_dotenv()

bot = get_bot_instance()
redis_client = get_redis_client()
LOGO = os.getenv("LOGO")


async def on_invitee_text_input(
    message: types.Message,
    state: FSMContext,
) -> None:
    """Manual invitee's username input processing."""
    input_text = message.text.strip()
    result = await resolve_invitee(message=message, username=input_text)

    if result["success"] == "link_ready":
        # clean up ['invitee username text input'] state
        await state.clear()
        await invitation_link_created_message(
            message=message,
            deep_link_text=result["message"],
        )
        inviter = message.from_user.username
        msg = f"{inviter} prepared invitation {LOGO} link for {input_text}"
        logging.info(msg)

    elif result["success"]:
        await state.clear()

        secure_id = ""
        inviter = UserDataResolver(message)
        invitee = result["invitee"]

        conversations = await redis_client.smembers(
            f"inviter_conversations:{inviter.id}",
        )
        if conversations:
            for conversation in conversations:
                stored_secure_id, stored_invitee_id = conversation.split(":")
                if stored_invitee_id == invitee.id:
                    secure_id = stored_secure_id
                    break

        fsm_manager = FSMStateManager(state)
        await fsm_manager.load()

        fsm_manager.secure_id = secure_id
        fsm_manager.inviter_id = inviter.id
        fsm_manager.invitee_id = invitee.id

        await fsm_manager.save()

        contacts, _ = await contacts_keyboard(inviter.id, inviter.username)
        await bot.send_message(
            inviter.id,
            f"Press button {invitee.username} to start {LOGO}!",
            reply_markup=contacts,
        )
        await bot.send_message(
            invitee.id,
            f"Waiting for {LOGO} with {inviter.username}.",
        )

        success_msg = (
            f"{LOGO} dialog @{inviter.username}/@{invitee.username} initiated."
        )
        logging.info(success_msg)

    else:
        await bot.send_message(message.chat.id, result["message"])
        logging.error(result["message"])
