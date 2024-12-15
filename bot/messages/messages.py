from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import StateFilter

from bot.commands.start import start_command
from bot.core.state import UsernameInputState
from bot.messages.invitee_text_input import on_invitee_text_input
from bot.messages.message_handler import handle_message

router = Router(name=__name__)

router.message.register(start_command, Command("start"))
router.message.register(
    on_invitee_text_input,
    StateFilter(UsernameInputState.entering_username),
)
router.message.register(handle_message)
