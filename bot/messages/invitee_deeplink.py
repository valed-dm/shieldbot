from aiogram.types import Message

from bot.utils.inviter_setup import inviter_setup


async def invitee_deep_link(message: Message, invitee: str) -> None:
    inviter_id = message.from_user.id
    secure_id = await inviter_setup(inviter_id)

    bot_username = "SecureTalkBot"
    deep_link = f"https://t.me/{bot_username}?start={secure_id}"
    info = f"SecureTalkBot invitation link for {invitee} is ready:\n{deep_link}"

    await message.answer(text=info)
