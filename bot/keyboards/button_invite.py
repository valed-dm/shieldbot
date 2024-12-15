from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

invite_partner_button = InlineKeyboardButton(
    text="Invite partner",
    callback_data="invite_for_securetalk",
)


def invite_button():
    return InlineKeyboardMarkup(inline_keyboard=[[invite_partner_button]])
