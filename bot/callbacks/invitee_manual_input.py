from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.core.state import UsernameInputState


async def on_manual_invitee_input(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    await state.set_state(UsernameInputState.entering_username)

    await callback_query.message.answer(
        "🔍 Please enter the username (starting with '@'):",
    )
