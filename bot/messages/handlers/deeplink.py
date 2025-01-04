import logging

from bot.keyboards.inviter_contacts_keyboard import contacts_keyboard
from bot.messages.handlers.base import BaseSecureTalkHandler
from bot.utils.invitee.resolve_invitation import resolve_invitation
from bot.utils.invitee.store_invitee import store_invitee

logger = logging.getLogger("DEEP_LINK_HANDLER")


class DeepLinkHandler(BaseSecureTalkHandler):
    async def message_controller(self):
        """Check for a '/start' command with a deep link invitation."""
        if len(self.text.split()) > 1:
            await self.load_securetalk_state()

            await self.resolve_deeplink()
            await self.store_invitation()
            await self.send_notifications()

            await self.set_securetalk_state()

            return True
        return False

    async def resolve_deeplink(self):
        """Verify and process a deep link invitation."""
        self._secure_id = self.text.split()[1]

        info_msg = f"{self.logo} Invitation from @{self.sender.username} received."
        logger.info(info_msg)

        try:
            self._inviter_id, self._inviter_username = await resolve_invitation(
                self._secure_id,
                self.sender.id,
            )
        except Exception as e:
            exception_msg = (
                f"Invitation is not resolved for "
                f"{self.logo} @{self.sender.username}: {e}"
            )
            logger.exception(exception_msg)
            error_msg = f"An error occurred while resolving {self.logo} invitation: {e}"
            raise ValueError(error_msg) from e

    async def store_invitation(self):
        """Store invitee and initialize FSM state."""
        if not self._inviter_id:
            error_msg = "Inviter ID is missing after invitation resolution."
            raise ValueError(error_msg)

        self._invitee_id = self.sender.id

        await store_invitee(self._secure_id, self.sender)

    async def send_notifications(self):
        """Send notifications to inviter and invitee."""
        if not self._inviter_id or not self._inviter_username:
            error_msg = "Incomplete inviter data for notification."
            raise ValueError(error_msg)

        contacts, _ = await contacts_keyboard(
            int(self._inviter_id),
            self._inviter_username,
        )
        await self.bot_instance.send_message(
            self._inviter_id,
            f"Press button '🔒 {self.sender.username}' to start {self.logo}.",
            reply_markup=contacts,
        )
        await self.bot_instance.send_message(
            self.sender.id,
            f"Now waiting for {self.logo} with @{self._inviter_username} to start.",
        )
        info_msg = (
            f"{self.logo} @{self._inviter_username} invitation resolved successfully: "
            f"{self.sender.id}:@{self.sender.username}"
        )
        logger.info(info_msg)
