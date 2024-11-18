from aiogram import Dispatcher
from aiogram.filters import Command

from bot.handlers import message_handler
from bot.handlers.menu import start_command


def register_messages(dp: Dispatcher):
    dp.message.register(start_command, Command("start"))
    dp.message.register(message_handler.handle_message)
