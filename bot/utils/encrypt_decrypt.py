import asyncio
import os

from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes


async def encrypt_message_with_aes(key: bytes, plaintext: str) -> bytes:
    """Encrypts message with symmetric key."""

    def sync_encrypt_message_with_aes():
        """Encrypts a message using AES."""
        iv = os.urandom(16)  # Initialization vector
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
        encryptor = cipher.encryptor()

        # Pad plaintext
        padder = sym_padding.PKCS7(128).padder()
        padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return iv + ciphertext  # Combine IV and ciphertext

    return await asyncio.to_thread(sync_encrypt_message_with_aes)


async def decrypt_message_with_aes(key: bytes, iv_ciphertext: bytes) -> str:
    """Decrypts message with symmetric key."""

    def sync_decrypt_message_with_aes():
        """Decrypts a message using AES."""
        iv = iv_ciphertext[:16]  # Extract IV
        ciphertext = iv_ciphertext[16:]

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove padding
        unpadder = sym_padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext.decode()

    return await asyncio.to_thread(sync_decrypt_message_with_aes)
