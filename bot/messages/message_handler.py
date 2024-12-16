from aiogram import types
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext

from bot.core.state import FSMStateManager
from bot.keys.aes.sym_key import retrieve_symmetric_key
from bot.keys.encrypt_decrypt import decrypt_message_with_aes
from bot.keys.encrypt_decrypt import encrypt_message_with_aes


async def handle_message(message: types.Message, state: FSMContext):
    fsm_manager = FSMStateManager(state)
    await fsm_manager.load()

    secure_id = fsm_manager.secure_id
    inviter_id = fsm_manager.inviter_id
    invitee_id = fsm_manager.invitee_id

    # Ensure the secure conversation is initialized
    if not secure_id:
        await message.reply("❌ Secure conversation is not initialized!")
        return

    # Determine the recipient
    sender_id = message.from_user.id
    if sender_id == int(inviter_id):
        recipient_id = invitee_id
    elif sender_id == int(invitee_id):
        recipient_id = inviter_id
    else:
        await message.reply("❌ You are not part of this secure conversation!")
        return

    # Retrieve symmetric key
    symmetric_key = retrieve_symmetric_key(conversation_id=secure_id)

    # Encrypt the message
    encrypted_text = await encrypt_message_with_aes(
        key=symmetric_key,
        plaintext=message.text,
    )

    # Send encrypted message to the recipient
    try:
        await message.bot.send_message(
            chat_id=recipient_id,
            text=f"🔒 Encrypted message from {message.from_user.username}: "
            f"{encrypted_text}",
        )
    except TelegramAPIError as e:
        await message.reply(f"❌ Failed to send message: {e!s}")
        return

    # For testing: decrypt and show back the original text (optional)
    decrypted_text = await decrypt_message_with_aes(
        key=symmetric_key,
        iv_ciphertext=encrypted_text,
    )
    await message.reply(f"🔓 Decrypted (for testing): {decrypted_text}")
