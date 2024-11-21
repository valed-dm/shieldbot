from aiogram import Dispatcher
from aiogram.filters import Command

from bot.commands.start import start_command_menu
from bot.messages.message_handler import handle_message
from bot.messages.partner_selected import on_partner_selected


def register_messages(dp: Dispatcher):
    dp.message.register(start_command_menu, Command("start"))
    dp.message.register(
        on_partner_selected,
        lambda message: message.text.startswith("@") or message.text.isdigit(),
    )
    dp.message.register(handle_message)
