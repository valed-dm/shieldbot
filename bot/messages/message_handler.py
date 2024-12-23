import logging
import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from bot.callbacks.data.redis_reference import create_callback_data
from bot.core.bot_instance import get_bot_instance
from bot.core.state import FSMStateManager
from bot.core.user_data_resolver import UserDataResolver
from bot.keyboards.button_decrypt import decrypt_button
from bot.keys.aes.sym_key import retrieve_symmetric_key
from bot.keys.encrypt_decrypt import encrypt_message_with_aes

load_dotenv()

logger = logging.getLogger("HANDLE_MESSAGE")

bot = get_bot_instance()
LOGO = os.getenv("LOGO")


async def handle_message(message: types.Message, state: FSMContext):
    """Handles secure message relay for both sender and recipient."""
    sender = UserDataResolver(message)

    fsm_manager = FSMStateManager(state)
    await fsm_manager.load()
    secure_id = fsm_manager.secure_id
    inviter_id = fsm_manager.inviter_id
    invitee_id = fsm_manager.invitee_id

    # Ensure the secure conversation is initialized
    if not secure_id:
        await message.reply(f"❌{LOGO} is not initialized!")
        return

    if sender.id not in (int(inviter_id), int(invitee_id)):
        await message.reply(f"❌You are not part of this {LOGO}!")
        return

    # Determine the recipient
    target = (
        (int(inviter_id), "invitee")
        if sender.id == int(invitee_id)
        else (int(invitee_id), "inviter")
    )
    recipient_id, recipient_role = target

    # Retrieve symmetric key
    symmetric_key = retrieve_symmetric_key(conversation_id=secure_id)

    try:
        encrypted_text = await encrypt_message_with_aes(
            key=symmetric_key,
            plaintext=message.text,
        )
        encrypted_hex = encrypted_text.hex()
        prefix = "ir:decrypt:" if recipient_role == "inviter" else "ie:decrypt:"

        callback_data = await create_callback_data(prefix, encrypted_hex)
        decrypt_btn = decrypt_button(callback_data)

        await message.bot.send_message(
            chat_id=recipient_id,
            text=f"@{sender.username} 🔑{encrypted_hex[:10]}..",
            reply_markup=decrypt_btn,
        )
        recipient = await bot.get_chat(recipient_id)
        await message.reply(
            f"@{sender.username} ciphered message to "
            f"@{recipient.username} was sent securely!",
        )

    except Exception as e:
        msg = f"❌Failed to send {LOGO} message: {e}"
        await message.reply(msg)
        logger.exception(msg)
