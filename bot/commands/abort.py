import logging
import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.core.bot_instance import get_bot_instance
from bot.messages.handlers.abort import AbortCommandHandler
from bot.messages.handlers.dispatcher import SecureTalkDispatcherHandler

load_dotenv()

logger = logging.getLogger("ABORT_COMMAND")

bot = get_bot_instance()
LOGO = os.getenv("LOGO")


async def abort_command(message: types.Message, state: FSMContext):
    dispatcher = SecureTalkDispatcherHandler(message, state, bot)
    if await dispatcher.message_controller():
        abort = AbortCommandHandler(message, state, bot)
        await abort.abort_command()
