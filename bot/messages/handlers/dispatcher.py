from bot.messages.handlers.base import BaseSecureTalkHandler


class SecureTalkDispatcherHandler(BaseSecureTalkHandler):
    async def message_controller(self):
        """Resolves conversation participant's roles."""
        await self.load_securetalk_state()
        # Check if secure conversation is initialized
        if not self._secure_id:
            await self.message.reply(f"❌{self.logo} is not initialized!")
            return False

        # Verify if the sender is part of the secure conversation
        if self.sender.id not in (int(self._inviter_id), int(self._invitee_id)):
            await self.message.reply(f"❌You are not part of this {self.logo}!")
            return False

        # Determine which side is target now
        target = (
            (int(self._inviter_id), "inviter", "ir")
            if self.sender.id == int(self._invitee_id)
            else (int(self._invitee_id), "invitee", "ie")
        )

        self.recipient_id, self.recipient_role, self.recipient_prefix = target
        self.sender_prefix = "ir" if self.recipient_prefix == "ie" else "ie"

        recipient = await self.bot_instance.get_chat(self.recipient_id)
        self.recipient_username = recipient.username

        await self.set_securetalk_state()
        return True
