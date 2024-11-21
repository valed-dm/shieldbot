from aiogram.types import InlineKeyboardButton

from bot.utils.dynamic_keyboard import dynamic_keyboard

main_menu_buttons = [
    InlineKeyboardButton(text="Help", callback_data="help"),
    InlineKeyboardButton(text="Start SecureTalk", callback_data="start_securetalk"),
    InlineKeyboardButton(text="Settings", callback_data="settings"),
]

main_menu_keyboard = dynamic_keyboard(main_menu_buttons, 3)
