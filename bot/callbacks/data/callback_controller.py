from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from bot.callbacks.data.redis_reference import get_callback_data
from bot.messages.handlers.base import BaseSecureTalkHandler

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram import types
    from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)


@dataclass
class CallbackData:
    """
    Represents the callback data structure.

    Attributes:
        role (str): The role of the user in the callback context, e.g.,
        'inviter' or 'invitee'.
        action (str): The action to be performed, extracted from the callback data.
        reference_id (str): The reference ID for retrieving data from Redis.
    """

    role: str = None
    action: str = None
    reference_id: str = None  # Callback reference id to get data from redis


class CallbackController(BaseSecureTalkHandler):
    """
    Controller for handling callback queries in a secure talk system.

    Attributes:
        raw_data (types.Message | types.CallbackQuery): The raw data from the callback.
        state (FSMContext): The FSM state for managing bot states.
        bot (Bot): The bot instance for interacting with Telegram API.
        attrs (CallbackData): Holds the parsed callback data.
    """

    def __init__(
        self,
        raw_data: types.Message | types.CallbackQuery,
        state: FSMContext,
        bot: Bot,
    ):
        """
        Initialize the CallbackController with a CallbackQuery, FSM state, and Bot
        instance.

        Args:
            raw_data (types.Message | types.CallbackQuery): Incoming data from the
            callback.
            state (FSMContext): Current state of the FSM for managing session state.
            bot (Bot): Instance of the bot for API interactions.
        """
        super().__init__(raw_data, state, bot)
        self.attrs = CallbackData()

    async def callback_controller(
        self,
        expected_prefix: str,
        params_count: int,
    ) -> bool:
        """
        Perform the callback handling process.

        Args:
            expected_prefix (str): The prefix that the callback data must start with.
            params_count (int): The expected number of parameters in the callback data.

        Returns:
            bool: True if the callback is valid, False otherwise.
        """
        # Validate callback data prefix
        if not self.callback_query.data.startswith(expected_prefix):
            await self.callback_query.answer("❌ Invalid callback data!")
            return False

        # Split callback data and extract the reference ID
        try:
            role_prefix, action, self.attrs.reference_id = (
                self.callback_query.data.split(
                    ":",
                    maxsplit=3,
                )
            )
            self.attrs.role = "inviter" if role_prefix == "ir" else "invitee"
            self.attrs.action = action
            self.callback_data = await get_callback_data(self.attrs.reference_id)

        except ValueError:
            await self.callback_query.answer("❌ Invalid callback structure!")
            return False

        # Validate callback data length
        if len(self.callback_data.split(":")) != params_count:
            msg = (
                f"❌ Invalid callback data format: "
                f"{len(self.callback_data.split(':'))} != {params_count}."
            )
            logger.warning(msg)
            await self.callback_query.answer(msg, show_alert=True)
            return False

        if self.attrs.action in ("invite", "accept", "decline"):
            self._extract_conversation_params()

        return True

    def _extract_conversation_params(self) -> None:
        """
        Extract and validate parameters from the callback data.

        Raises:
            ValueError: If the user ID in the callback data does not match the
            sender's ID.
        """
        (
            secure_id,
            inviter_id,
            inviter_username,
            invitee_id,
            invitee_username,
        ) = self.callback_data.split(":")

        comparison_id = inviter_id if self.attrs.role == "inviter" else invitee_id
        if str(self.sender.id) != comparison_id:
            msg = "❌ User ID mismatch in callback data."
            raise ValueError(msg)

        # Assign extracted parameters to instance attributes
        self.secure_talk_data.secure_id = secure_id
        self.secure_talk_data.inviter_id = int(inviter_id)
        self.secure_talk_data.inviter_username = inviter_username
        self.secure_talk_data.invitee_id = int(invitee_id)
        self.secure_talk_data.invitee_username = invitee_username

    @property
    def secure_id(self) -> str:
        """str: Secure ID associated with the callback data."""
        return self.secure_talk_data.secure_id

    @property
    def inviter_id(self) -> int:
        """int: The ID of the inviter in the conversation."""
        return self.secure_talk_data.inviter_id

    @property
    def inviter_username(self) -> str:
        """str: The username of the inviter in the conversation."""
        return self.secure_talk_data.inviter_username

    @property
    def invitee_id(self) -> int:
        """int: The ID of the invitee in the conversation."""
        return self.secure_talk_data.invitee_id

    @property
    def invitee_username(self) -> str:
        """str: The username of the invitee in the conversation."""
        return self.secure_talk_data.invitee_username

    @property
    def reference_id(self) -> str:
        """str: The redis storage reference ID extracted from the callback data."""
        return self.attrs.reference_id

    @property
    def role(self) -> str:
        """str: The role of the user in the conversation, e.g.,
        'inviter' or 'invitee'."""
        return self.attrs.role
