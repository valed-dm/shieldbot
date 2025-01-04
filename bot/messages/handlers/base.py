from __future__ import annotations

import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv

from bot.core.state import FSMStateManager
from bot.core.user_data_resolver import UserDataResolver

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram import types
    from aiogram.fsm.context import FSMContext


load_dotenv()

LOGO = os.getenv("LOGO")


class BaseMessageHandler:
    def __init__(
        self,
        message: types.Message,
        state: FSMContext,
        bot: Bot,
        logo=f"{LOGO}",
    ):
        self.bot_instance = bot
        self.message = message
        self.text = message.text
        self.state = state
        self.logo = logo
        self.secure_id = None
        self.inviter_id = None
        self.inviter_username = None
        self.invitee_id = None
        self.invitee_username = None
        self.sender = UserDataResolver(message)
        self.sender_prefix = None
        self.recipient_username = None
        self.recipient_id = None
        self.recipient_role = None
        self.recipient_prefix = None

    async def message_controller(self):
        """Default verification logic."""
        error_msg = "Subclasses must implement this method"
        raise NotImplementedError(error_msg)

    async def load_securetalk_state(self):
        fsm_manager = FSMStateManager(self.state)
        await fsm_manager.load()

        self.secure_id = fsm_manager.secure_id
        self.inviter_id = fsm_manager.inviter_id
        self.inviter_username = fsm_manager.inviter_username
        self.invitee_id = fsm_manager.invitee_id
        self.invitee_username = fsm_manager.invitee_username
        self.sender_prefix = fsm_manager.sender_prefix
        self.recipient_username = fsm_manager.recipient_username
        self.recipient_id = fsm_manager.recipient_id
        self.recipient_role = fsm_manager.recipient_role
        self.recipient_prefix = fsm_manager.recipient_prefix

    async def set_securetalk_state(self):
        fsm_manager = FSMStateManager(self.state)
        await fsm_manager.load()

        fsm_manager.secure_id = self.secure_id
        fsm_manager.inviter_id = self.inviter_id
        fsm_manager.inviter_username = self.inviter_username
        fsm_manager.invitee_id = self.sender.id
        fsm_manager.invitee_username = self.invitee_username
        fsm_manager.sender_prefix = self.sender_prefix
        fsm_manager.recipient_username = self.recipient_username
        fsm_manager.recipient_id = self.recipient_id
        fsm_manager.recipient_role = self.recipient_role
        fsm_manager.recipient_prefix = self.recipient_prefix

        await fsm_manager.save()
