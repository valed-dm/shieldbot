from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import CallbackQuery

from bot.callbacks.confirm_button_click import on_confirm_button_click
from bot.callbacks.generate_rsa_keypair import generate_keypair_callback
from bot.callbacks.invitee_button_input import on_invitee_button_click
from bot.callbacks.invitee_manual_input import on_manual_invitee_input
from bot.callbacks.invitees_reset import on_reset_invitees
from bot.commands.help import help_callback
from bot.commands.securetalk import on_secure_talk_start
from bot.commands.settings import on_settings

CALLBACK_HELP = "help"
CALLBACK_SETTINGS = "settings"
CALLBACK_GENERATE_KEYPAIR = "generate_keypair"
CALLBACK_SEND_PUBLIC_KEY = "send_public_key"
CALLBACK_START_SECURETALK = "start_securetalk"
CALLBACK_SAVED_INVITEE_INPUT = "ir:"
CALLBACK_ACCEPT_INVITATION = "ie:"
CALLBACK_MANUAL_INVITEE_INPUT = "invite_for_securetalk"
CALLBACK_RESET_INVITEES = "reset_invitees"

router = Router(name=__name__)


class CallbackFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, callback_query: CallbackQuery) -> bool:
        return callback_query.data == self.my_text


router.callback_query.register(
    help_callback,
    CallbackFilter(CALLBACK_HELP),
)
router.callback_query.register(
    on_settings,
    CallbackFilter(CALLBACK_SETTINGS),
)
router.callback_query.register(
    generate_keypair_callback,
    CallbackFilter(CALLBACK_GENERATE_KEYPAIR),
)
router.callback_query.register(
    on_secure_talk_start,
    CallbackFilter(CALLBACK_SEND_PUBLIC_KEY),
)
router.callback_query.register(
    on_secure_talk_start,
    CallbackFilter(CALLBACK_START_SECURETALK),
)
router.callback_query.register(
    on_invitee_button_click,
    lambda c: c.data.startswith(CALLBACK_SAVED_INVITEE_INPUT),
)
router.callback_query.register(
    on_confirm_button_click,
    lambda c: c.data.startswith(CALLBACK_ACCEPT_INVITATION),
)
router.callback_query.register(
    on_manual_invitee_input,
    CallbackFilter(CALLBACK_MANUAL_INVITEE_INPUT),
)
router.callback_query.register(
    on_reset_invitees,
    CallbackFilter(CALLBACK_RESET_INVITEES),
)
