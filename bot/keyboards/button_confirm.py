from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


def confirm_button(securetalk_data: str):
    button = InlineKeyboardButton(
        text="Accept 🔒SecureTalk",
        callback_data=securetalk_data,
    )
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
