from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from bot.core.bot_instance import get_bot_instance
from bot.utils.resolve_invitee import resolve_invitee_id

if TYPE_CHECKING:
    from aiogram import types
    from aiogram.fsm.context import FSMContext

bot = get_bot_instance()


async def on_partner_selected(message: types.Message, state: FSMContext) -> None:
    input_text = message.text.strip()

    result = await resolve_invitee_id(message=message, username=input_text)

    if result["success"] == "link_ready":
        await bot.send_message(message.chat.id, result["message"])
        await state.clear()

        logging.info(result["message"].split("\n")[1])

    elif result["success"]:
        invitee_id = result["partner_id"]

        await bot.send_message(invitee_id, "SecureTalk initiated!")
        await state.clear()

        success_msg = f"Invitee found: ID {invitee_id}."
        logging.info(success_msg)

    else:
        await bot.send_message(message.chat.id, result["message"])

        logging.error(result["message"])
