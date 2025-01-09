"""Abort command handler."""

import logging
import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.core.bot_instance import get_bot_instance
from bot.messages.handlers.abort import AbortCommandHandler
from bot.messages.handlers.dispatcher import SecureTalkDispatcherHandler

load_dotenv()

logger = logging.getLogger("ABORT_COMMAND")

bot = get_bot_instance()
LOGO = os.getenv("LOGO")


async def abort_command(message: types.Message, state: FSMContext):
    """
    Handle the '/abort' command to reset or cancel an active SecureTalk session.

    This function is triggered when a user sends the '/abort' command. It ensures that
    any ongoing SecureTalk session is properly cleaned up and the state is reset.

    The command utilizes two handlers:
        1. `SecureTalkDispatcherHandler` - Validates and manages the message context.
        2. `AbortCommandHandler` - Performs the actual abort logic for SecureTalk
        sessions.

    :param message: The incoming message containing the '/abort' command.
    :type message: types.Message
    :param state: The FSM context for managing the current user's state.
    :type state: FSMContext

    Workflow:
        1. Initializes a `SecureTalkDispatcherHandler` to validate the message.
        2. If validation passes, invokes the `AbortCommandHandler` to handle the session
        abort.
        3. Resets or cleans up the session as per the handler logic.

    Example Usage:
        User sends the '/abort' command:
        - Active SecureTalk session is terminated.
        - User receives a confirmation message or feedback indicating the operation's
        success.

    Error Handling:
        - Assumes proper validation of the message by `SecureTalkDispatcherHandler`.
        - Any exceptions during the abort process should be managed by the
        `AbortCommandHandler`.

    Dependencies:
        - `SecureTalkDispatcherHandler`: Ensures the message context is valid for
        SecureTalk.
        - `AbortCommandHandler`: Contains the logic for aborting active SecureTalk
        sessions.

    """
    dispatcher = SecureTalkDispatcherHandler(message, state, bot)
    if await dispatcher.message_controller():
        abort = AbortCommandHandler(message, state, bot)
        await abort.abort_command()
