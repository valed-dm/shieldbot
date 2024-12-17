import os

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

LOGO = os.getenv("LOGO")


def confirm_button(securetalk_data: str):
    button = InlineKeyboardButton(
        text=f"✅{LOGO}",
        callback_data=securetalk_data,
    )
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
