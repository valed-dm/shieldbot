from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


def dynamic_menu_keyboard(buttons_per_row: int):
    buttons = [
        InlineKeyboardButton(text="Help", callback_data="help"),
        InlineKeyboardButton(text="Generate Keypair", callback_data="generate_keypair"),
        InlineKeyboardButton(text="Start SecureTalk", callback_data="start_securetalk"),
        InlineKeyboardButton(text="Settings", callback_data="settings"),
    ]

    rows = [
        buttons[i : i + buttons_per_row]
        for i in range(0, len(buttons), buttons_per_row)
    ]

    return InlineKeyboardMarkup(inline_keyboard=rows)


async def start_command(message: types.Message):
    await message.answer(
        "Welcome to SecureTalk! Choose an action below:",
        reply_markup=dynamic_menu_keyboard(3),
    )
