from bot.callbacks.data.redis_reference import create_callback_data
from bot.keyboards.button_abort import abort_button
from bot.messages.handlers.base import BaseMessageHandler


class AbortCommandHandler(BaseMessageHandler):
    async def abort_command(self):
        await self.load_securetalk_state()

        recipient_close_callback_data = await create_callback_data(
            f"{self.recipient_prefix}:abort:",
            self.secure_id,
        )
        sender_close_callback_data = await create_callback_data(
            f"{self.sender_prefix}:abort:",
            self.secure_id,
        )

        recipient_close_btn = abort_button(recipient_close_callback_data)
        sender_close_btn = abort_button(sender_close_callback_data)

        abort_message = f"Abort {self.logo}?"
        await self.message.bot.send_message(
            chat_id=self.recipient_id,
            text=abort_message,
            reply_markup=recipient_close_btn,
        )
        await self.message.reply(
            text=abort_message,
            reply_markup=sender_close_btn,
        )
