from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


def decrypt_button(role_action_id: str):
    button = InlineKeyboardButton(
        text="🔑Decrypt",
        callback_data=role_action_id,
    )
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
