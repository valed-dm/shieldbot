from __future__ import annotations

import logging

from aiogram.exceptions import TelegramBadRequest

from bot.core.bot_instance import bot


async def resolve_partner_id(chat_id: int, input_text: str) -> int | None:
    """
    Resolves the Telegram user ID of a partner from a given username or input text.

    :param chat_id: SecureTalk chat id
    :param input_text: The input text from the user (e.g., username or contact name).
    :return: The partner's Telegram ID if resolved, otherwise None.
    """
    # Ensure the input starts with '@' (Telegram usernames format)
    if not input_text.startswith("@") and not input_text.isdigit():
        await bot.send_message(
            chat_id=chat_id,
            text="Invalid username format. Usernames must start with '@'. "
            "Please try again.",
        )
        return None

    username = input_text.strip()

    try:
        user = await bot.get_chat(username)
    except TelegramBadRequest as e:
        if "chat not found" in str(e):
            await bot.send_message(
                chat_id=chat_id,
                text=f"Could not find the user '{username}'. "
                f"Please check the username and try again.",
            )
        else:
            msg = f"TelegramBadRequest occurred: {e}"
            logging.exception(msg)
        return None
    except Exception as e:
        msg = f"Error resolving partner ID: {e}"
        logging.exception(msg)
        await bot.send_message(
            chat_id=chat_id,
            text="An unexpected error occurred while resolving the partner ID. "
            "Please try again later.",
        )
        return None
    else:
        return user.id
