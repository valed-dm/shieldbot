from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import CallbackQuery

from bot.callbacks.generate_rsa_keypair import generate_keypair_callback
from bot.callbacks.partner_selected import on_manual_partner_input
from bot.callbacks.partner_selected import on_partner_selected
from bot.commands.help import help_callback
from bot.commands.securetalk import on_secure_talk_start

CALLBACK_HELP = "help"
CALLBACK_GENERATE_KEYPAIR = "generate_keypair"
CALLBACK_SEND_PUBLIC_KEY = "send_public_key"
CALLBACK_START_SECURETALK = "start_securetalk"
CALLBACK_MANUAL_PARTNER_INPUT = "manual_partner_input"

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
    on_partner_selected,
    lambda c: c.data.startswith("partner_"),
)
router.callback_query.register(
    on_manual_partner_input,
    CallbackFilter(CALLBACK_MANUAL_PARTNER_INPUT),
)
