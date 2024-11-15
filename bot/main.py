import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv

from bot.handlers import message_handler
from bot.handlers.menu import help_callback
from bot.handlers.menu import menu_command
from bot.handlers.menu import start_conversation_callback

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Register handlers
dp.message.register(menu_command, Command("start"))  # Start command shows the main menu
dp.message.register(message_handler.handle_message)
dp.callback_query.register(
    start_conversation_callback,
    lambda c: c.data == "start_conversation",
)
dp.callback_query.register(help_callback, lambda c: c.data == "help")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
