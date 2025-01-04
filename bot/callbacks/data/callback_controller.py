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
    role: str = None
    action: str = None
    reference_id: str = None  # Callback reference id to get data from redis


class CallbackController(BaseSecureTalkHandler):
    def __init__(
        self,
        raw_data: types.Message | types.CallbackQuery,
        state: FSMContext,
        bot: Bot,
    ):
        """
        Initialize the verifier with a callback query and FSM state.
        """
        super().__init__(raw_data, state, bot)
        self.attrs = CallbackData()

    async def callback_controller(
        self,
        expected_prefix: str,
        params_count: int,
    ) -> bool:
        """
        Perform the callback verification process.

        :param expected_prefix: The prefix that the callback data must start with.
        :param params_count: The expected number of parameters in the callback data.
        :return: True if verification is successful, False otherwise.
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

        if self.attrs.action in ("invite", "accept"):
            self._extract_conversation_params()

        return True

    def _extract_conversation_params(self) -> None:
        """
        Extract and validate parameters from the callback data.
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
        return self.secure_talk_data.secure_id

    @property
    def inviter_id(self) -> int:
        return self.secure_talk_data.inviter_id

    @property
    def inviter_username(self) -> str:
        return self.secure_talk_data.inviter_username

    @property
    def invitee_id(self) -> int:
        return self.secure_talk_data.invitee_id

    @property
    def invitee_username(self) -> str:
        return self.secure_talk_data.invitee_username

    @property
    def reference_id(self) -> str:
        return self.attrs.reference_id

    @property
    def role(self) -> str:
        return self.attrs.role
