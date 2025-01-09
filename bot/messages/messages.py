from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import StateFilter

from bot.commands.abort import abort_command
from bot.commands.start import start_command
from bot.core.state import UsernameInputState
from bot.messages.handlers.on_message import handle_message
from bot.messages.invitee.username_input import on_username_input

router = Router(name=__name__)

router.message.register(start_command, Command("start"))
router.message.register(abort_command, Command("abort"))
router.message.register(
    on_username_input,
    StateFilter(UsernameInputState.entering_username),
)
router.message.register(handle_message)
