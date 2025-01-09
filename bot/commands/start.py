from __future__ import annotations

from typing import TYPE_CHECKING

from bot.core.bot_instance import get_bot_instance
from bot.messages.handlers.deeplink import DeepLinkHandler
from bot.messages.handlers.start import StartCommandHandler

if TYPE_CHECKING:
    from aiogram import types
    from aiogram.fsm.context import FSMContext

bot = get_bot_instance()


async def start_command(message: types.Message, state: FSMContext):
    start = StartCommandHandler(message, state, bot)
    if not await start.message_controller():
        deep_link = DeepLinkHandler(message, state, bot)
        await deep_link.message_controller()
