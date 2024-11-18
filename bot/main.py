import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from dotenv import load_dotenv

from bot.handlers.callbacks import register_callbacks
from bot.handlers.messages import register_messages

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
if API_TOKEN is None:
    msg = "BOT_TOKEN not found! Check your .env file."
    raise ValueError(msg)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    register_messages(dp)
    register_callbacks(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
