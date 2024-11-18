from aiogram import Dispatcher

from .callbacks_logic import generate_keypair_callback
from .callbacks_logic import help_callback
from .callbacks_logic import start_conversation_callback

CALLBACK_HELP = "help"
CALLBACK_GENERATE_KEYPAIR = "generate_keypair"
CALLBACK_START_CONVERSATION = "start_securetalk"


def register_callbacks(dp: Dispatcher):
    dp.callback_query.register(help_callback, lambda c: c.data == CALLBACK_HELP)
    dp.callback_query.register(
        generate_keypair_callback,
        lambda c: c.data == CALLBACK_GENERATE_KEYPAIR,
    )
    dp.callback_query.register(
        start_conversation_callback,
        lambda c: c.data == CALLBACK_START_CONVERSATION,
    )
