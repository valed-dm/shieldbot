"""Module for Keychain/Keystore Integration"""

import asyncio
import os

import keyring
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key


def generate_symmetric_key() -> bytes:
    """Generates a 256-bit symmetric key for AES."""
    return os.urandom(32)  # AES-256 requires a 32-byte key


def save_symmetric_key(conversation_id: str, symmetric_key: bytes) -> None:
    """Saves the symmetric key securely in Keychain/Keystore."""
    keyring.set_password("SecureTalk", conversation_id, symmetric_key.hex())


def retrieve_symmetric_key(conversation_id: str) -> bytes:
    """Retrieves the symmetric key from Keychain/Keystore."""
    hex_key = keyring.get_password("SecureTalk", conversation_id)
    if hex_key is None:
        msg = "No symmetric key found for this conversation."
        raise ValueError(msg)
    return bytes.fromhex(hex_key)


async def encrypt_symmetric_key_with_rsa(public_key_pem: bytes, symmetric_key: bytes):
    """Symmetric key is encrypted with public key to be safely passed to other party."""
    if isinstance(public_key_pem, str):
        public_key_pem = public_key_pem.encode("utf-8")

    def sync_encrypt_symmetric_key_with_rsa():
        """Encrypts the symmetric key with the recipient's public RSA key."""
        public_key = load_pem_public_key(public_key_pem)
        encrypted_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return encrypted_key

    return await asyncio.to_thread(sync_encrypt_symmetric_key_with_rsa)


async def decrypt_symmetric_key_with_rsa(private_key_pem: bytes, encrypted_key: bytes):
    if isinstance(private_key_pem, str):
        private_key_pem = private_key_pem.encode("utf-8")

    def sync_decrypt_symmetric_key_with_rsa():
        from cryptography.hazmat.primitives.serialization import load_pem_private_key

        private_key = load_pem_private_key(private_key_pem, password=None)
        symmetric_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return symmetric_key

    return await asyncio.to_thread(sync_decrypt_symmetric_key_with_rsa)
