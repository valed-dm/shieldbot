from aiogram import types

from bot.keyboards.contacts_keyboard import contacts_keyboard


async def on_secure_talk_start(callback_query: types.CallbackQuery):
    user_contacts = await contacts_keyboard(callback_query.from_user.id)

    await callback_query.message.answer(
        "🔒 Who do you want to initiate SecureTalk with? "
        "Please share the username or choose from your contacts.",
        reply_markup=user_contacts,
    )
