from aiogram import Dispatcher

from bot.callbacks.generate_rsa_keypair import generate_keypair_callback
from bot.callbacks.partner_selected import on_manual_partner_input
from bot.callbacks.partner_selected import on_partner_selected
from bot.commands.help import help_callback
from bot.commands.start_securetalk import on_secure_talk_start

CALLBACK_HELP = "help"
CALLBACK_GENERATE_KEYPAIR = "generate_keypair"
CALLBACK_SEND_PUBLIC_KEY = "send_public_key"
CALLBACK_START_SECURETALK = "start_securetalk"
CALLBACK_MANUAL_PARTNER_INPUT = "manual_partner_input"


def register_callbacks(dp: Dispatcher):
    dp.callback_query.register(help_callback, lambda c: c.data == CALLBACK_HELP)
    dp.callback_query.register(
        generate_keypair_callback,
        lambda c: c.data == CALLBACK_GENERATE_KEYPAIR,
    )
    dp.callback_query.register(
        on_secure_talk_start,
        lambda c: c.data == CALLBACK_SEND_PUBLIC_KEY,
    )
    dp.callback_query.register(
        on_secure_talk_start,
        lambda c: c.data == CALLBACK_START_SECURETALK,
    )
    dp.callback_query.register(
        on_partner_selected,
        lambda c: c.data.startswith("partner_"),
    )
    dp.callback_query.register(
        on_manual_partner_input,
        lambda c: c.data == CALLBACK_MANUAL_PARTNER_INPUT,
    )
