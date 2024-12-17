"""Not in use now. Module was conceived for manual public key exchange"""

from aiogram import Bot
from aiogram import types

from bot.keys.rsa.rsa_key import generate_rsa_keypair


async def generate_keypair_callback(callback_query: types.CallbackQuery, bot: Bot):
    """Provides user with public/private key pair for secure chat."""
    private_key, public_key = await generate_rsa_keypair()
    # Send the keys to the user (private key securely)
    await bot.send_message(
        callback_query.from_user.id,
        "🔑 Your RSA Public Key:\n" + public_key.decode(),
    )
    await bot.send_message(
        callback_query.from_user.id,
        "⚠️ Keep your Private Key safe:\n" + private_key.decode(),
    )
    await callback_query.message.answer("[🔑🔑]:RSA keypair generated successfully!")
    await callback_query.answer()
