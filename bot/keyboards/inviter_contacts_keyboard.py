from __future__ import annotations

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from bot.callbacks.data.redis_reference import create_callback_data
from bot.core.bot_instance import get_bot_instance
from bot.core.redis_client import get_redis_client
from bot.utils.dynamic_keyboard import dynamic_keyboard
from bot.utils.inviter.inviter_partners import get_inviter_partners

bot = get_bot_instance()
redis_client = get_redis_client()


async def contacts_keyboard(
    inviter_id: int,
    inviter_username: str,
) -> tuple[InlineKeyboardMarkup, int]:
    """
    Generates an InlineKeyboardMarkup for the user's contacts.

    Args:
        user_id (int): The Telegram user ID of the current user.

    Returns tuple:
        InlineKeyboardMarkup: A keyboard with contact options.
        Integer: Contacts quantity.
        :param inviter_id: Telegram user id of the inviter.
        :param inviter_username: Telegram username of the inviter.
    """
    contacts = await get_inviter_partners(inviter_id)
    contacts_menu_buttons = [
        InlineKeyboardButton(
            text=f"🔒 {contact['username']}",
            callback_data=await create_callback_data(
                "ir:invite:",
                contact["secure_id"],
                inviter_id,
                inviter_username,
                contact["invitee_id"],
                contact["username"],
            ),
        )
        for contact in contacts
    ]

    return dynamic_keyboard(contacts_menu_buttons, 3), len(contacts)
