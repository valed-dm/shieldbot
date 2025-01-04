from __future__ import annotations

import os
from typing import TYPE_CHECKING

from aiogram import types
from dotenv import load_dotenv

from bot.core.state import FSMStateManager
from bot.core.user_data_resolver import UserDataResolver

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.fsm.context import FSMContext


load_dotenv()

LOGO = os.getenv("LOGO")


class BaseSecureTalkHandler:
    def __init__(
        self,
        incoming_data: types.Message | types.CallbackQuery,
        state: FSMContext,
        bot: Bot,
        logo=f"{LOGO}",
    ):
        self.bot_instance = bot
        self.message = (
            incoming_data if isinstance(incoming_data, types.Message) else None
        )
        self.callback_query = (
            incoming_data if isinstance(incoming_data, types.CallbackQuery) else None
        )
        self.callback_data = None
        self.text = self.message.text if self.message else None
        self.state = state
        self.logo = logo
        self._secure_id = None
        self._inviter_id = None
        self._inviter_username = None
        self._invitee_id = None
        self._invitee_username = None
        self.sender = UserDataResolver(incoming_data)
        self.sender_prefix = None
        self.recipient_username = None
        self.recipient_id = None
        self.recipient_role = None
        self.recipient_prefix = None

    async def message_controller(self):
        """Default verification logic."""
        error_msg = "Subclasses must implement this method"
        raise NotImplementedError(error_msg)

    async def sync_securetalk_state(self, mode: str):
        """
        Synchronize secure talk state between FSM manager and instance attributes.

        Args:
            mode (str): Either "load" to load data into the instance or
                        "set" to save data to the FSM manager.
        """
        if mode not in {"load", "set"}:
            error_msg = f"Unsupported mode: {mode}"
            raise ValueError(error_msg)

        attributes_map: dict[str, str] = {
            "secure_id": "_secure_id",
            "inviter_id": "_inviter_id",
            "inviter_username": "_inviter_username",
            "invitee_id": "_invitee_id",
            "invitee_username": "_invitee_username",
            "sender_prefix": "sender_prefix",
            "recipient_username": "recipient_username",
            "recipient_id": "recipient_id",
            "recipient_role": "recipient_role",
            "recipient_prefix": "recipient_prefix",
        }

        fsm_manager = FSMStateManager(self.state)
        await fsm_manager.load()

        for fsm_attr, instance_attr in attributes_map.items():
            if mode == "load":
                setattr(self, instance_attr, getattr(fsm_manager, fsm_attr))
            elif mode == "set":
                setattr(fsm_manager, fsm_attr, getattr(self, instance_attr))

        await fsm_manager.save()

    async def load_securetalk_state(self):
        await self.sync_securetalk_state(mode="load")

    async def set_securetalk_state(self):
        await self.sync_securetalk_state(mode="set")

    async def abort_securetalk_state(self) -> tuple[str, str]:
        """
        Clears the FSM state and returns usernames of inviter and invitee.

        Returns:
            tuple[str, str]: Inviter's username and invitee's username.
        """
        fsm_manager = FSMStateManager(self.state)
        await fsm_manager.load()

        inviter_username = fsm_manager.inviter_username
        invitee_username = fsm_manager.invitee_username

        await fsm_manager.clear()
        await fsm_manager.save()

        return inviter_username, invitee_username
