from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.exceptions import TelegramAPIError
from aiogram.exceptions import TelegramBadRequest

from bot.core.bot_instance import get_bot_instance
from bot.messages.invitee.invitee_deeplink import invitee_deep_link
from bot.messages.messages_predefined import invalid_format
from bot.messages.messages_predefined import invitation_link_created
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
            await invitee_deep_link(message=message, invitee=username)
            return {
                "success": "link_ready",
                "message": invitation_link_created(username),
            }

        return {"success": False, "message": unexpected_err_msg(username, e)}

    except TelegramAPIError as e:
        return {"success": False, "message": unexpected_err_msg(username, e)}

    else:
        return {"success": True, "invitee": invitee}
