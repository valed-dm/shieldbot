import os

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

LOGO = os.getenv("LOGO")


def confirm_button(role_action_id: str):
    button = InlineKeyboardButton(
        text=f"✅{LOGO}",
        callback_data=role_action_id,
    )
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
