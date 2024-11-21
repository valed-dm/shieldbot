from __future__ import annotations

from typing import TYPE_CHECKING

from bot.keyboards.menu_keyboard import main_menu_keyboard

if TYPE_CHECKING:
    from aiogram import types


async def start_command_menu(message: types.Message):
    await message.answer(
        "Welcome to SecureTalk! Choose an action below:",
        reply_markup=main_menu_keyboard,
    )
