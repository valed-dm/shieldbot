from __future__ import annotations

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from bot.utils.dynamic_keyboard import dynamic_keyboard


async def contacts_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Generates an InlineKeyboardMarkup for the user's contacts.

    Args:
        user_id (int): The Telegram user ID of the current user.

    Returns:
        InlineKeyboardMarkup: A keyboard with contact options.
    """
    # Fetch contacts for the current user (replace with real data)
    contacts = await get_user_contacts(user_id)

    contacts_menu_buttons = [
        InlineKeyboardButton(
            text=f"🔒 {contact['username']}",
            callback_data=f"partner_{contact['id']}",
        )
        for contact in contacts
    ]

    # Add manual input option
    contacts_menu_buttons.append(
        InlineKeyboardButton(
            text="🔍 Enter username manually",
            callback_data="manual_partner_input",
        ),
    )

    return dynamic_keyboard(contacts_menu_buttons, 3)


async def get_user_contacts(user_id: int) -> list[dict]:
    """
    Mock function to get user contacts.

    Args:
        user_id (int): The Telegram user ID.

    Returns:
        list[dict]: A list of contacts with IDs and usernames.
    """
    return [
        {"id": 101, "username": "secure_buddy1"},
        {"id": 202, "username": "secure_buddy2"},
        {"id": 303, "username": "secure_buddy3"},
        {"id": 404, "username": "secure_buddy4"},
        {"id": 505, "username": "secure_buddy5"},
        {"id": 606, "username": "secure_buddy6"},
    ]
