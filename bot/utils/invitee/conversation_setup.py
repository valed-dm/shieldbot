from bot.core.redis_client import get_redis_client
from bot.keys.aes.sym_key import encrypt_symmetric_key_with_rsa
from bot.keys.aes.sym_key import generate_symmetric_key
from bot.keys.aes.sym_key import save_symmetric_key
from bot.keys.exchange.key_status import notify_key_ready
from bot.utils.inviter.inviter_conversations import store_inviter_conversations

TTL = 3600


redis_client = get_redis_client()


async def conversation_setup(
    inviter_public_pem: bytes,
    inviter_id: int,
    invitee_id: int,
    secure_id: str,
) -> bool:
    """Prepares conversation data on invitee side."""
    conv_setup = await redis_client.get(f"{secure_id}:conversation_setup")

    if conv_setup != "in_progress":
        msg = "Invalid or already set up conversation!"
        raise ValueError(msg)

    # Invitee generates symmetric key
    symmetric_key = generate_symmetric_key()

    # Saves the symmetric key securely in local invitee Keychain/Keystore.
    save_symmetric_key(conversation_id=secure_id, symmetric_key=symmetric_key)

    encrypted_symmetric_key = await encrypt_symmetric_key_with_rsa(
        inviter_public_pem,
        symmetric_key,
    )

    # Encrypted symmetric key prepared by invitee for the inviter's usage.
    await redis_client.setex(
        f"{secure_id}:encrypted_key",
        TTL,
        encrypted_symmetric_key.hex(),
    )

    await store_inviter_conversations(secure_id, inviter_id, invitee_id)

    await redis_client.set(f"{secure_id}:conversation_setup", "set_up")

    # Notifies inviter that symmetric key is ready to be processed
    await notify_key_ready(inviter_id, secure_id)

    return True
