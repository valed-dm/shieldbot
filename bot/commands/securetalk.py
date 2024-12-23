import os

from aiogram import types
from dotenv import load_dotenv

from bot.core.user_data_resolver import UserDataResolver
from bot.keyboards.button_invite import invite_button
from bot.keyboards.inviter_contacts_keyboard import contacts_keyboard

load_dotenv()

LOGO = os.getenv("LOGO")


async def on_prepare_secure_talk(callback_query: types.CallbackQuery):
    inviter = UserDataResolver(callback_query)
    contacts_markup, contacts_qty = await contacts_keyboard(
        inviter.id,
        inviter.username,
    )

    text_invite = (
        f"Invite a partner for {LOGO} from the list;\n"
        f"Use 'Settings:Invite partner' if empty."
    )

    if contacts_qty != 0:
        await callback_query.message.answer(
            text_invite,
            reply_markup=contacts_markup,
        )
    else:
        invite_partner_keyboard = invite_button()
        await callback_query.message.answer(
            f"No active {LOGO}s. Invite a partner.",
            reply_markup=invite_partner_keyboard,
        )
