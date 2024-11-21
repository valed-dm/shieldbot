import asyncio
import os
from base64 import urlsafe_b64decode
from base64 import urlsafe_b64encode

import aiofiles
from aiogram import types
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


async def generate_rsa_keypair():
    def sync_rsa_keypair_generation():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
        public_key = private_key.public_key()

        # Serialize keys
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return private_pem, public_pem

    return await asyncio.to_thread(sync_rsa_keypair_generation)


async def encrypt_private_key(private_key: bytes, passphrase: str) -> bytes:
    def sync_encrypt_private_key():
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        key = kdf.derive(passphrase.encode())
        encrypted_key = urlsafe_b64encode(salt + key + private_key)
        return encrypted_key

    return await asyncio.to_thread(sync_encrypt_private_key)


async def decrypt_private_key(encrypted_key: bytes, passphrase: str) -> bytes:
    def sync_decrypt_private_key():
        decoded = urlsafe_b64decode(encrypted_key)
        salt, key, private_key = decoded[:16], decoded[16:48], decoded[48:]
        kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        derived_key = kdf.derive(passphrase.encode())
        if derived_key != key:
            msg = "Incorrect passphrase."
            raise ValueError(msg)
        return private_key

    return await asyncio.to_thread(sync_decrypt_private_key)


async def download_private_key(callback_query: types.CallbackQuery, private_key: bytes):
    file_path = "private_key.pem"

    async with aiofiles.open(file_path, mode="wb") as file:
        await file.write(private_key)

    # Send the file to the user
    await callback_query.message.answer_document(
        types.InputFile(file_path),
        caption="🔑 Here is your private key. Keep it secure!",
    )
