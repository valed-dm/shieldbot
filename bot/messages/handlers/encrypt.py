import logging

from bot.callbacks.data.redis_callback_data import create_callback_data
from bot.keyboards.button_decrypt import decrypt_button
from bot.keys.aes.sym_key import retrieve_symmetric_key
from bot.keys.encrypt_decrypt import encrypt_message_with_aes
from bot.messages.handlers.base import BaseSecureTalkHandler

logger = logging.getLogger("ENCRYPTOR_HANDLER")


class SecureTalkEncryptorHandler(BaseSecureTalkHandler):
    async def encrypt_message(self):
        await self.load_securetalk_state()

        symmetric_key = retrieve_symmetric_key(
            conversation_id=self.secure_talk_data.secure_id,
        )

        try:
            encrypted_text = await encrypt_message_with_aes(
                key=symmetric_key,
                plaintext=self.text,
            )
            encrypted_hex = encrypted_text.hex()

            callback_data = await create_callback_data(
                f"{self.secure_talk_data.recipient_prefix}:decrypt:",
                encrypted_hex,
            )

            decrypt_btn = decrypt_button(callback_data)

            await self.message.bot.send_message(
                chat_id=self.secure_talk_data.recipient_id,
                text=f"@{self.sender.username} 🔑{encrypted_hex[:10]}..",
                reply_markup=decrypt_btn,
            )
            await self.message.reply(
                f"@{self.sender.username} ciphered message to "
                f"@{self.secure_talk_data.recipient_username} was sent securely!",
            )

        except Exception as e:
            msg = f"❌Failed to send {self.logo} message: {e}"
            await self.message.reply(msg)
            logger.exception(msg)
