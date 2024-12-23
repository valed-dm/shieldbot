from aiogram.types import InlineKeyboardButton

from bot.keyboards.button_invite import invite_partner_button
from bot.utils.dynamic_keyboard import dynamic_keyboard

reset_partners_button = InlineKeyboardButton(
    text="Reset partners",
    callback_data="ir:reset:",
)

settings_menu_buttons = [invite_partner_button, reset_partners_button]

settings_menu_keyboard = dynamic_keyboard(settings_menu_buttons, 3)
