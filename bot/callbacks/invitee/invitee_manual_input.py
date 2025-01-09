"""Module initiates manual invitee's username input"""

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.core.state import UsernameInputState


async def on_manual_invitee_input(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """
    Initiates the manual entry of the invitee's username.

    This function transitions the FSM to the `UsernameInputState.entering_username`
    state and prompts the user to input the invitee's username manually.

    :param callback_query: The callback query that triggered the manual input workflow.
    :type callback_query: types.CallbackQuery
    :param state: The current finite state machine (FSM) context.
    :type state: FSMContext

    :return: None
    """
    await state.set_state(UsernameInputState.entering_username)

    await callback_query.message.answer(
        "🔍 Please enter @username:",
    )
