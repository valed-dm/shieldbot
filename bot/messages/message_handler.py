from aiogram import types

from bot.keys.sym_key import retrieve_symmetric_key
from bot.utils.encrypt_decrypt import decrypt_message_with_aes
from bot.utils.encrypt_decrypt import encrypt_message_with_aes


async def handle_message(message: types.Message, conversation_id: str):
    symmetric_key = retrieve_symmetric_key(conversation_id=conversation_id)
    encrypted_text = await encrypt_message_with_aes(
        key=symmetric_key,
        plaintext=message.text,
    )
    await message.reply(f"Encrypted: {encrypted_text}")

    # Decrypting the message back (for testing purposes)
    decrypted_text = await decrypt_message_with_aes(
        key=symmetric_key,
        iv_ciphertext=encrypted_text,
    )
    await message.reply(f"Decrypted: {decrypted_text}")
