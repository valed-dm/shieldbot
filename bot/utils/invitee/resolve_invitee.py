from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.exceptions import TelegramAPIError
from aiogram.exceptions import TelegramBadRequest

from bot.core.bot_instance import get_bot_instance
from bot.messages.invitee.deeplink_builder import invitee_deep_link
from bot.messages.messages_predefined import invalid_format
from bot.messages.messages_predefined import unexpected_err_msg

if TYPE_CHECKING:
    from aiogram.types import Message

bot = get_bot_instance()


async def resolve_invitee(message: Message, username: str):
    """
    Resolves the invitee's unique Telegram ID using their username.
    Ensures the username is valid and invitee is accessible to the bot.
    """
    if not username.startswith("@"):
        return {"success": False, "message": invalid_format()}

    try:
        invitee = await bot.get_chat(username)

    except TelegramBadRequest as e:
        if "chat not found" in str(e):
            deep_link_text = await invitee_deep_link(message, invitee=username)
            return {
                "success": "link_ready",
                "message": deep_link_text,
            }

        return {"success": False, "message": unexpected_err_msg(username, e)}

    except TelegramAPIError as e:
        return {"success": False, "message": unexpected_err_msg(username, e)}

    else:
        return {"success": True, "invitee": invitee}
