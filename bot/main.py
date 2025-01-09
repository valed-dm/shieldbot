import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.callbacks.callbacks import router as callbacks_router
from bot.core.bot_instance import get_bot_instance
from bot.core.redis_client import close_redis_client
from bot.core.redis_client import get_redis_client
from bot.messages.messages import router as messages_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("SecureTalkBot")

bot = get_bot_instance()
redis_client = get_redis_client()

dp = Dispatcher(storage=MemoryStorage())


async def on_shutdown():
    """Shutdown tasks."""
    await close_redis_client()
    logger.info("Shutting down redis connection")
    await bot.session.close()
    logger.info("Bot session closed.")


async def main():
    """SecureTalk Bot entry point"""
    dp.include_router(messages_router)
    dp.include_router(callbacks_router)

    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
