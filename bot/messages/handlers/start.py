import logging

from bot.keyboards.main_menu_keyboard import main_menu_keyboard
from bot.keys.aes.sym_pipe import sym_exchange_cycle
from bot.messages.handlers.base import BaseMessageHandler
from bot.utils.inviter.inviter_workflow import initialize_inviter_workflow

logger = logging.getLogger("START_HANDLER")


class StartCommandHandler(BaseMessageHandler):
    async def message_controller(self):
        """Check for a '/start' command."""
        if self.text == "/start":
            await self.start_command()
            return True
        return False

    async def start_command(self):
        try:
            await initialize_inviter_workflow(self.sender.id)
            await self.message.answer(
                f"Welcome to {self.logo}!",
                reply_markup=main_menu_keyboard,
            )
            await sym_exchange_cycle(self.sender.id)
        except Exception as e:
            exception_msg = f"Error initializing RSA keys: {e}"
            logger.exception(exception_msg)
            await self.message.answer("An error occurred. Please try again.")
