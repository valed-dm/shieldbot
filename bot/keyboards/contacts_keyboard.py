from __future__ import annotations

import json

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from bot.core.bot_instance import bot
from bot.core.redis_client import get_redis_client
from bot.utils.dynamic_keyboard import dynamic_keyboard

redis_client = get_redis_client()


async def contacts_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Generates an InlineKeyboardMarkup for the user's contacts.

    Args:
        user_id (int): The Telegram user ID of the current user.

    Returns:
        InlineKeyboardMarkup: A keyboard with contact options.
    """
    contacts = await get_inviter_partners(inviter_id=user_id)

    contacts_menu_buttons = [
        InlineKeyboardButton(
            text=f"🔒 {contact['username']}",
            callback_data=f"partner_{contact['invitee_id']}",
        )
        for contact in contacts
    ]

    contacts_menu_buttons.append(
        InlineKeyboardButton(
            text="🔍 Invite partner",
            callback_data="manual_partner_input",
        ),
    )

    return dynamic_keyboard(contacts_menu_buttons, 3)


async def get_inviter_partners(inviter_id: int):
    secure_ids = await redis_client.smembers(f"inviter_conversations:{inviter_id}")
    invitees = []

    if not secure_ids:
        await bot.send_message(
            inviter_id,
            "You do not have active secured contacts yet.!",
        )
    else:
        for secure_id in secure_ids:
            invitee_data_json = await redis_client.get(
                f"conversation_invitee:{secure_id}",
            )
            if invitee_data_json:
                invitees.append(json.loads(invitee_data_json))

    return invitees
