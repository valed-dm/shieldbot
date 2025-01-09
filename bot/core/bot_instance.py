import os
from functools import lru_cache

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")

if API_TOKEN is None:
    msg = "BOT_TOKEN not found! Check your .env file."
    raise ValueError(msg)


@lru_cache(maxsize=1)
def get_bot_instance() -> Bot:
    return Bot(token=API_TOKEN)
