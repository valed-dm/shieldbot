from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import StateFilter

from bot.commands.start import start_command
from bot.core.state import UsernameInputState
from bot.messages.message_handler import handle_message
from bot.messages.partner_selected import on_partner_selected

router = Router(name=__name__)

router.message.register(start_command, Command("start"))
router.message.register(
    on_partner_selected,
    StateFilter(UsernameInputState.entering_username),
)
router.message.register(handle_message)
