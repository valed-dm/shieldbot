import logging
import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.core.bot_instance import get_bot_instance
from bot.messages.handlers.dispatcher import SecureTalkDispatcherHandler
from bot.messages.handlers.encrypt import SecureTalkEncryptorHandler

load_dotenv()

logger = logging.getLogger("HANDLE_MESSAGE")

bot = get_bot_instance()
LOGO = os.getenv("LOGO")


async def handle_message(message: types.Message, state: FSMContext):
    """Handles secure message relay for both sender and recipient."""
    dispatcher = SecureTalkDispatcherHandler(message, state, bot)
    if await dispatcher.message_controller():
        encryptor = SecureTalkEncryptorHandler(message, state, bot)
        await encryptor.encrypt_message()
