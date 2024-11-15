from aiogram import types

from bot.utils.pki_manager import decrypt_message
from bot.utils.pki_manager import encrypt_message


async def handle_message(message: types.Message):
    # Placeholder example of using encryption for message
    encrypted_text = encrypt_message(message.text)
    await message.reply(f"Encrypted: {encrypted_text}")

    # Decrypting the message back (for demo purposes)
    decrypted_text = decrypt_message(encrypted_text)
    await message.reply(f"Decrypted: {decrypted_text}")
