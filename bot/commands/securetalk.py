from aiogram import types

from bot.core.user_data_resolver import UserDataResolver
from bot.keyboards.button_invite import invite_button
from bot.keyboards.inviter_contacts_keyboard import contacts_keyboard


async def on_secure_talk_start(callback_query: types.CallbackQuery):
    inviter = UserDataResolver(callback_query)
    contacts_markup, contacts_qty = await contacts_keyboard(
        inviter.id,
        inviter.username,
    )

    if contacts_qty != 0:
        await callback_query.message.answer(
            "Invite a partner for 🔒SecureTalk from list below;\n"
            "Use 'Settings'->'Invite partner' if not found in a list.",
            reply_markup=contacts_markup,
        )
    else:
        invite_partner_keyboard = invite_button()
        await callback_query.message.answer(
            "You have not active partners. Invite a partner for 🔒SecureTalk.",
            reply_markup=invite_partner_keyboard,
        )
