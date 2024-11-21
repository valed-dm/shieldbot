from aiogram import types


async def on_partner_selected(callback_query: types.CallbackQuery):
    partner_id = int(callback_query.data.split("_")[1])
    await callback_query.message.answer(f"✅ Partner selected: {partner_id}")


async def on_manual_partner_input(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "🔍 Please enter the username or ID of your partner:",
    )
