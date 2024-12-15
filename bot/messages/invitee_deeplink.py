import os

from aiogram.types import Message
from dotenv import load_dotenv

from bot.utils.inviter_setup import inviter_setup
from bot.utils.user_data_resolver import UserDataResolver

load_dotenv()

LOGO = os.getenv("LOGO")


async def invitee_deep_link(message: Message, invitee: str) -> None:
    inviter = UserDataResolver(message)

    secure_id = await inviter_setup(inviter.id, inviter.username)

    bot_username = "SecureTalkBot"
    deep_link = f"https://t.me/{bot_username}?start={secure_id}"

    deep_link_text = (
        f"{LOGO} link for '{invitee}' from '@{inviter.username}':\n{deep_link}"
    )
    await message.answer(text=deep_link_text)
