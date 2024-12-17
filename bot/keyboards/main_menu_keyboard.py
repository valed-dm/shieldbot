import os

from aiogram.types import InlineKeyboardButton
from dotenv import load_dotenv

from bot.utils.dynamic_keyboard import dynamic_keyboard

load_dotenv()

LOGO = os.getenv("LOGO")

main_menu_buttons = [
    InlineKeyboardButton(text=f"Prepare {LOGO}", callback_data="prepare_securetalk"),
    InlineKeyboardButton(text="Settings", callback_data="settings"),
    InlineKeyboardButton(text="Help", callback_data="help"),
]

main_menu_keyboard = dynamic_keyboard(main_menu_buttons, 2)
