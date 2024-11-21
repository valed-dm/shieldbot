import logging

from aiogram import Dispatcher

from bot.callbacks.callbacks import register_callbacks
from bot.core.bot_instance import bot
from bot.messages.messages import register_messages

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


async def main():
    """SecureTalk Bot"""
    dp = Dispatcher()

    register_messages(dp)
    register_callbacks(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
