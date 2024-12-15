from uuid import uuid4

import keyring

from bot.core.redis_client import get_redis_client

redis_client = get_redis_client()


async def inviter_setup(inviter_id: int, inviter_username: str, ttl=3600):
    secure_id = str(uuid4())

    public_key_hex = keyring.get_password("SecureTalk_PublicKey", str(inviter_id))
    if public_key_hex is None:
        msg = f"No public key found for inviter ID {inviter_id}."
        raise ValueError(msg)

    await redis_client.setex(
        f"{secure_id}:inviter_data",
        ttl,
        f"{inviter_id}:{inviter_username}:{public_key_hex}",
    )

    await redis_client.setex(f"{secure_id}:conversation_setup", ttl, "in_progress")

    return secure_id
