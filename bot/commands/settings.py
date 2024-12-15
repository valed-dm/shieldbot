from aiogram import types

from bot.keyboards.settings_keyboard import settings_menu_keyboard


async def on_settings(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "Settings options available:",
        reply_markup=settings_menu_keyboard,
    )
