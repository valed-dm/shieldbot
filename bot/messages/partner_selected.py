from aiogram import types

from bot.utils.resolve_partner import resolve_partner_id


async def on_partner_selected(message: types.Message):
    partner_id = await resolve_partner_id(
        chat_id=message.chat.id,
        input_text=message.text,
    )
    if not partner_id:
        await message.reply("❌ User not found or not registered with the bot.")
        return
