import os

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")

if API_TOKEN is None:
    msg = "BOT_TOKEN not found! Check your .env file."
    raise ValueError(msg)

# Initialize bot instance
bot = Bot(token=API_TOKEN)
