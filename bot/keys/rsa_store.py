import asyncio

import keyring


async def rsa_store(
    inviter_id: int,
    private_key: bytes,
    public_key: bytes,
):
    """Asynchronously saves private/public keys securely."""

    def sync_store_keys():
        keyring.set_password(
            "SecureTalk_PrivateKey",
            str(inviter_id),
            private_key.hex(),
        )
        keyring.set_password(
            "SecureTalk_PublicKey",
            str(inviter_id),
            public_key.hex(),
        )

    await asyncio.to_thread(sync_store_keys)


def sync_retrieve_private_key(inviter_id: int) -> bytes:
    """Retrieves the symmetric key from Keychain/Keystore."""
    hex_key = keyring.get_password("SecureTalk_PrivateKey", str(inviter_id))

    if hex_key is None:
        msg = f"No private key exists for user {inviter_id}."
        raise ValueError(msg)

    return bytes.fromhex(hex_key)
